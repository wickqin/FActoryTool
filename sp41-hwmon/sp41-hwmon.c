#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include <signal.h>
#include <unistd.h>
#include <dirent.h>

#define EC_RAM_FILE     "/sys/kernel/debug/ec/ec0/io"
#define CPU_TEMP_ADR    0x3E //CPU 温度的偏移地址，一个字节
#define FAN_SP_ADR      0x50 //风扇速度的偏移地址，两个字节

#define SLEEP_TIME      3
#define HWON_PATH       "/sys/class/hwmon"
#define HWON_NAME       "hwmon"
#define NAME            "name"
#define TZ_APCI         "acpitz"
#define TZ_ACPI_TEMP    "temp1_input"

static volatile sig_atomic_t stop = 0;
static void interrupt_handler(int sig)
{
    stop = 1;
}

//读取主板温度
static int read_acpi_tz(unsigned int* acpi_tz)
{
    int hown_device_count, i;
    size_t strlen;
    char acpi_tz_file_name[256];
    char acpi_tz_temp_name[256];
    char read_buf[256];
    FILE *fp_name, *fp_temp;
    DIR *dir;
    struct dirent *ent;

    dir = opendir(HWON_PATH);
    if(dir == NULL)
    {
        printf("Open %s error,exit\n", HWON_PATH);
        return -1;
    }

    hown_device_count = 0;
    while ((ent = readdir (dir)) != NULL)
    {
        hown_device_count++;
    }

    closedir (dir);
    if(hown_device_count == 0)
    {
        printf("Acpitz not found\n");
        return 0;
    }

    *acpi_tz = 0xFF;
    for(i = 0;i < hown_device_count - 2; i++) //-2 是因为目录下的 “.” 和 ".." 也被算进来了
    {
        snprintf(acpi_tz_file_name, sizeof(acpi_tz_file_name), "%s/%s%d/%s",
                HWON_PATH, HWON_NAME, i, NAME);

        fp_name = fopen(acpi_tz_file_name, "r");
        if(fp_name == NULL)
            continue;

        strlen = fread(read_buf, 1, sizeof(read_buf) - 1, fp_name);
        read_buf[strlen - 1] = 0x00;//读出来的内容最后的字节是 0x0a(LF)，要截掉这个 0x0a
        fclose(fp_name);

        if(strcmp(read_buf, TZ_APCI) == 0)
        {
            snprintf(acpi_tz_temp_name, sizeof(acpi_tz_temp_name), "%s/%s%d/%s",
                    HWON_PATH, HWON_NAME, i, TZ_ACPI_TEMP);
            fp_temp = fopen(acpi_tz_temp_name, "r");
            if(fp_temp == NULL)
                continue;

            strlen = fread(read_buf, 1, sizeof(read_buf) - 1, fp_temp);
            read_buf[strlen - 1] = 0x00;//读出来的内容最后的字节是 0x0a(LF)，要截掉这个 0x0a
            fclose(fp_temp);

            *acpi_tz = atoi(read_buf) / 1000;
            break;
        }
    }

    if(*acpi_tz == 0xFF)
    {
        printf("Read ACPI TZ error!\n");
        return -2;
    }

    return 0;
}

//读取风扇转速 & CPU 温度
static int read_ec_ram(unsigned char* cpu_temp, unsigned short* fan_speed)
{
    FILE *fp_ec_ram;
    size_t ret,retval;
    unsigned short fan_spee_tmp;

    fp_ec_ram = fopen(EC_RAM_FILE,"r");
    if(fp_ec_ram == NULL)
    {
        printf("Read %s error,exit\n", EC_RAM_FILE);
        return -1;
    }
        
    ret = fseek(fp_ec_ram ,FAN_SP_ADR, SEEK_SET);
    if(ret != 0)
    {
        printf("Fan speed: Seek EC io error\n");
        retval = -2;
        goto error;
    }

    ret= fread(&fan_spee_tmp, sizeof(short), 1, fp_ec_ram); //offset = 0x50
    if(ret != 1)
    {
        printf("Read fan speed hight byte error!ret = %zu\n", ret);
        retval = -3;
        goto error;
    }

    ret = fseek(fp_ec_ram ,CPU_TEMP_ADR, SEEK_SET);
    if(ret != 0)
    {
        printf("CPU temperature: Seek EC io error\n");
        retval = -2;
        goto error;
    }

    ret= fread(cpu_temp , sizeof(char), 1, fp_ec_ram);
    if(ret != 1)
    {
        printf("Read CPU temperature error!ret = %zu\n", ret);
        retval = -3;
        goto error;
    }

    //风扇速度是两个 byte(Address: 0x50 and 0x51)，在 EC RAM 读出来的风扇速度是大端字节序，但是 Intel 平台是小端字节序.
    //例如： "/sys/kernel/debug/ec/ec0/io" 中读出来的数据是(Addres 0x50:FAN_SP_ADR) 0xA313，这是大端字节序数据.
    //Intel 平台因为是小端字节序，所以需要做一次大/低端字节序的转换，也就是在 Intel 平台上真实的数据是 0x13A3.
    *fan_speed = ((fan_spee_tmp & 0x00FF) << 8) | ((fan_spee_tmp & 0xFF00) >> 8);
    
    //printf("Read byte = 0x%X,0x%X,0x%X\n", *cpu_temp, *fan_speed, fan_spee_tmp);

    fclose(fp_ec_ram);
    return 0;

error:
    fclose(fp_ec_ram);
    return retval;
}

int main(int argc, char* argv[])
{
    unsigned short fan_speed;
    unsigned char  cpu_temp;
    unsigned int   acpi_tz;

    signal(SIGINT, interrupt_handler);  //如果按下 Ctrl+C，停止 while(!stop) 循环
    signal(SIGTERM, interrupt_handler); //如果收到 kill 信号，停止 while(!stop) 循环

    fan_speed = 0;
    cpu_temp  = 0;

    read_ec_ram(&cpu_temp, &fan_speed);
    read_acpi_tz(&acpi_tz);

    // printf("CPU temperature      = %d\n", cpu_temp);
    // printf("ACPI TZ temperature  = %d\n", acpi_tz);
    // printf("Speed of the fan     = %d\n\n", fan_speed);
    printf("%d\n",fan_speed);
    return 0;
}