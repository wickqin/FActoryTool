#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/io.h>
#define VERSION      "1.0.3"

#define EC_RAM_FILE "/sys/kernel/debug/ec/ec0/io"

#define EC_VER_HIG_OFFSET  0x00
#define EC_VER_LOW_OFFSET  0x01
static int read_ec_version(unsigned char* ec_ver_high,unsigned char* ec_ver_low)
{
    FILE *fp;
    int  ret, retval;

    retval = 0;
    fp = fopen(EC_RAM_FILE,"r");
    if(fp == NULL)
    {
        printf("sp41x6g-fw-ver : Set-EC : Open EC io error\n");
        return -1;
    }

    ret = fseek(fp ,EC_VER_HIG_OFFSET, SEEK_SET);
    if(ret != 0)
    {
        printf("sp41x6g-fw-ver : Set-EC : Seek EC io error\n");
        retval = -2;
        goto fun_exit;
    }

    ret= fread(ec_ver_high , 1, 1, fp);
    if(ret != 1)
    {
        printf("sp41x6g-fw-ver : Set-EC : Read EC io (High byte)error = %d\n", ret);
        retval = -3;
        goto fun_exit;
    }

    ret = fseek(fp ,EC_VER_LOW_OFFSET, SEEK_SET);
    if(ret != 0)
    {
        printf("sp41x6g-fw-ver : Set-EC : Seek EC io error\n");
        retval = -2;
        goto fun_exit;
    }

    ret= fread(ec_ver_low, 1, 1, fp);
    if(ret != 1)
    {
        printf("sp41x6g-fw-ver : Set-EC : Read EC io error = %d\n", ret);
        retval = -3;
        goto fun_exit;
    }

fun_exit:
    fflush(fp);
    fclose(fp);
    return retval;
}

void ITE_INIT(void)  // Set EC DLM start from 0xC000
{

    unsigned short inaddr;
    unsigned char value;
    unsigned char SioPort;

    value = 0x80;
    inaddr = 0x1060;
    SioPort = 0x4E;
    outb(0x2E,SioPort);
    outb(0x11,SioPort+1);	
    outb(0x2F,SioPort);
    outb(inaddr/256,SioPort+1);
    outb(0x2E,SioPort);
    outb(0x10,SioPort+1);	
    outb(0x2F,SioPort);
    outb(inaddr%256, SioPort+1);
    outb(0x2E,SioPort);
    outb(0x12,SioPort+1);	
    outb(0x2F,SioPort);
    outb(value,SioPort+1); 
}


unsigned char ReadECRam(unsigned short inaddr)
{
    unsigned char SioPort;

    SioPort = 0x4E;
    outb(0x2E,SioPort);
    outb(0x11,SioPort+1);	
    outb(0x2F,SioPort);
    outb(inaddr/256,SioPort+1);
    outb(0x2E,SioPort);
    outb(0x10,SioPort+1);	
    outb(0x2F,SioPort);
    outb(inaddr%256, SioPort+1);
    outb(0x2E,SioPort);
    outb(0x12,SioPort+1);	
    outb(0x2F,SioPort);
    return (inb(SioPort+1));   
}



void WriteECRam(unsigned short inaddr, unsigned char value)
{
    unsigned char SioPort;

    SioPort = 0x4E;
    outb(0x2E,SioPort);
    outb(0x11,SioPort+1);	
    outb(0x2F,SioPort);
    outb(inaddr/256,SioPort+1);
    outb(0x2E,SioPort);
    outb(0x10,SioPort+1);	
    outb(0x2F,SioPort);
    outb(inaddr%256, SioPort+1);
    outb(0x2E,SioPort);
    outb(0x12,SioPort+1);	
    outb(0x2F,SioPort);
    outb(value,SioPort+1); 
}


int main(int argc,char** argv)
{
    unsigned char ec_ver_low, ec_ver_high;
    int ret;
    unsigned char pdfw_ver_byte0, pdfw_ver_byte1;
    unsigned char pdfw_ver_low_bit, pdfw_ver_high_bit;

//Read EC version
    ret = read_ec_version(&ec_ver_high, &ec_ver_low);
    if(ret != 0)
    {
        printf("EC version read failed = %d！\n", ret);
        return 0;  
    }
    printf("EC version: %02d.%02d\n", ec_ver_high, ec_ver_low);
//Read EC version,end


//Read PD FW version
    // 請求對 I/O 埠 0x3f8 的訪問權限:
    if(ioperm(0x4E, 1, 1) < 0)
    {
        perror("ioperm");
        return 1;
    }

    if(ioperm(0x4F, 1, 1) < 0)
    {
        perror("ioperm");
        return 1;
    }

    ITE_INIT();
    WriteECRam(0xd5b0, 0x40);
    sleep(1);
    pdfw_ver_byte0 = ReadECRam(0xd5b1);
    pdfw_ver_byte1 = ReadECRam(0xd5b2);

    pdfw_ver_high_bit = (pdfw_ver_byte1 >> 4) & 0x0F;
    pdfw_ver_low_bit  = pdfw_ver_byte1 & 0x0F;
    printf("PD Version: V%01X.%01X.%02X\n", pdfw_ver_high_bit, pdfw_ver_low_bit, pdfw_ver_byte0);

    //printf("PD Version: %x.%x\n",ReadECRam(0xd5b1),ReadECRam(0xd5b2));
//Read PD FW version,end

    return 0;
}

