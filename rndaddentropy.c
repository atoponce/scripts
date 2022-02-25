/* rndaddentropy, an RNDADDENTROPY ioctl wrapper
 * Copyright (C) 2012-2021 Ryan Finnie <ryan@finnie.org>
 * SPDX-License-Identifier: MPL-2.0
 */

#include <stdio.h>
#include <string.h>
#include <sys/fcntl.h>
#include <sys/ioctl.h>
#include <linux/random.h>

int main(int argc, char *argv[]) {
  struct {
    int entropy_count;
    int buf_size;
    char buf[1024];
  } entropy;

  int i;
  for(i=1; i < argc; i++) {
    if(strcmp(argv[i], "--help") == 0) {
      fprintf(stderr, "rndaddentropy, an RNDADDENTROPY ioctl wrapper\n");
      fprintf(stderr, "Copyright (C) 2012 Ryan Finnie <ryan@finnie.org>\n");
      fprintf(stderr, "\n");
      fprintf(stderr, "Usage: $ENTROPY_GENERATOR | rndaddentropy\n");
      fprintf(stderr, "\n");
      fprintf(stderr, "WARNING!  This program is dangerous, and relies on your entropy\n");
      fprintf(stderr, "generator producing adequate output.  Inadequate entropy generation\n");
      fprintf(stderr, "fed to the primary pool is a security risk to the system.\n");
      return(1);
    }
  }

  int randfd;
  if((randfd = open("/dev/random", O_WRONLY)) < 0) {
    perror("/dev/random");
    return(1);
  }

  int count;
  while((count = fread(entropy.buf, 1, sizeof(entropy.buf), stdin)) > 0) {
    entropy.entropy_count = count * 8;
    entropy.buf_size = count;
    if(ioctl(randfd, RNDADDENTROPY, &entropy) < 0) {
      perror("RNDADDENTROPY");
      return(1);
    }
  }

  return(0);
}
