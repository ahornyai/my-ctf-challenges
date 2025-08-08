#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <linux/seccomp.h>
#include <linux/filter.h>
#include <linux/audit.h>
#include <sys/prctl.h>
#include <sys/syscall.h>
#include <stddef.h>

#define ArchField offsetof(struct seccomp_data, arch)
#define SyscallField offsetof(struct seccomp_data, nr)

void init() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
}

void enable_seccomp() {
    struct sock_filter filter[] = { // [255, 255 ,255 ,255, 255]
        // Load the architecture
        { 0x20, 0x00, 0x00, ArchField },
        // Check if the architecture is x86_64
        { 0x15, 0x00, 0x1c, AUDIT_ARCH_X86_64 },
        // Load the syscall number
        { 0x20, 0x00, 0x00, SyscallField },
        // If syscall number >= 0x40000000, check if it's invalid
        { 0x35, 0x00, 0x01, 0x40000000 },
        { 0x15, 0x00, 0x19, 0xffffffff },
        // List of forbidden syscalls
        { 0x15, 0x18, 0x00, __NR_open },
        { 0x15, 0x17, 0x00, __NR_close },
        { 0x15, 0x16, 0x00, __NR_pwrite64 },
        { 0x15, 0x15, 0x00, __NR_writev },
        { 0x15, 0x14, 0x00, __NR_pipe },
        { 0x15, 0x13, 0x00, __NR_dup },
        { 0x15, 0x12, 0x00, __NR_dup2 },
        { 0x15, 0x11, 0x00, __NR_sendfile },
        { 0x15, 0x10, 0x00, __NR_socket },
        { 0x15, 0x0f, 0x00, __NR_sendto },
        { 0x15, 0x0e, 0x00, __NR_sendmsg },
        { 0x15, 0x0d, 0x00, __NR_bind },
        { 0x15, 0x0c, 0x00, __NR_clone },
        { 0x15, 0x0b, 0x00, __NR_fork },
        { 0x15, 0x0a, 0x00, __NR_vfork },
        { 0x15, 0x09, 0x00, __NR_execve },
        { 0x15, 0x08, 0x00, __NR_ptrace },
        { 0x15, 0x07, 0x00, __NR_splice },
        { 0x15, 0x06, 0x00, __NR_tee },
        { 0x15, 0x05, 0x00, __NR_dup3 },
        { 0x15, 0x04, 0x00, __NR_pipe2 },
        { 0x15, 0x03, 0x00, __NR_pwritev },
        { 0x15, 0x02, 0x00, __NR_process_vm_writev },
        { 0x15, 0x01, 0x00, __NR_execveat },
        // Allow all other syscalls
        { 0x06, 0x00, 0x00, SECCOMP_RET_ALLOW },
        // Kill forbidden syscalls
        { 0x06, 0x00, 0x00, SECCOMP_RET_KILL },
    };

    struct sock_fprog prog = {
        .len = (unsigned short)(sizeof(filter) / sizeof(filter[0])),
        .filter = filter,
    };

    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0)) {
        perror("prctl(PR_SET_NO_NEW_PRIVS)");
        exit(EXIT_FAILURE);
    }

    if (prctl(PR_SET_SECCOMP, SECCOMP_MODE_FILTER, &prog)) {
        perror("prctl(PR_SET_SECCOMP)");
        exit(EXIT_FAILURE);
    }
}

void dev_null() {
    char buffer[8];

    puts("[/dev/null as a service] Send us anything, we won't do anything with it.");
    enable_seccomp();

    gets(buffer);
}

int main() {
    init();

    dev_null();
    return 0;
}
