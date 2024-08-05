#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/kthread.h>
#include <linux/sched.h>
#include <linux/time.h>

int init_module (void) {

int p;
int q=7;
int r=8;

p=q+r;

printk (KERN_INFO "The result is: %d", p);

return 0;

}

void cleanup_module(void) {
printk(KERN_INFO"BYE\n");
}
