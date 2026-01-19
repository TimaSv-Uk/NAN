#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>

#include "read_file_bites_dynamically/read_file_bites.h"

void find_neighbors_assignment5(bites_t *point_in, bites_t *point_out, int a) {
  size_t n = point_in->bite_lenght;
  point_out->bites[0] = (unsigned char)(point_in->bites[0] + a);
  char x0 = point_in->bites[0];

  for (int i = 1; i < n; i++) {
    if (i % 2 == 0) {
      point_out->bites[i] =
          (unsigned char)(point_in->bites[i] -
                          point_out->bites[0] * point_in->bites[i - 1]);
    } else {
      point_out->bites[i] =
          (unsigned char)(point_in->bites[i] - x0 * point_out->bites[i - 1]);
    }
  }
}

void reverse_find_neighbors_assignment5(bites_t *point_in, bites_t *point_out,
                                        int a) {
  size_t n = point_in->bite_lenght;
  point_out->bites[0] = (unsigned char)(point_in->bites[0] - a);
  unsigned char x0 = point_out->bites[0];
  unsigned char y0 = point_in->bites[0];

  for (int i = 1; i < n; i++) {
    if (i % 2 == 0) {

      point_out->bites[i] =
          (unsigned char)(point_in->bites[i] + y0 * point_out->bites[i - 1]);
    } else {

      point_out->bites[i] =
          (unsigned char)(point_in->bites[i] + x0 * point_in->bites[i - 1]);
    }
  }
}
bites_t *encode_assignment5(bites_t *vector, int d_mod_range) {

  size_t bites_length = vector->bite_lenght;

  // bites_t current_state = *vector;

  // bites_t current_state;
  // current_state.bite_lenght = bites_length;
  // current_state.bites = malloc(bites_length);

  // for (int i = 0; i < current_state.bite_lenght; i++) {
  //   current_state.bites[i] = vector->bites[i];
  // }
  //
  bites_t next_state;
  next_state.bite_lenght = bites_length;
  next_state.bites = malloc(bites_length);
  if (!next_state.bites) {
    fprintf(stderr, "Memory allocation failed\n");
    return NULL;
  }

  for (int a = 0; a < d_mod_range; a++) {
    find_neighbors_assignment5(vector, &next_state, a);
    unsigned char *temp = vector->bites;
    vector->bites = next_state.bites;
    next_state.bites = temp;
  }
  free(next_state.bites);
  return vector;
}

bites_t *decode_assignment5(bites_t *vector, int d_mod_range) {

  size_t bites_length = vector->bite_lenght;

  // bites_t current_state = *vector;

  // bites_t current_state;
  // current_state.bite_lenght = bites_length;
  // current_state.bites = malloc(bites_length);
  // for (int i = 0; i < current_state.bite_lenght; i++) {
  //   current_state.bites[i] = vector->bites[i];
  // }

  bites_t next_state;
  next_state.bite_lenght = bites_length;
  next_state.bites = malloc(bites_length);

  for (int a = d_mod_range - 1; a >= 0; a--) {
    reverse_find_neighbors_assignment5(vector, &next_state, a);
    unsigned char *temp = vector->bites;
    vector->bites = next_state.bites;
    next_state.bites = temp;
  }
  free(next_state.bites);
  return vector;
}

int main() {
  bites_t file_bites;
  // char *file_name = "bob.txt";
  // char *file_name = "vid_2mb.mp4";
  char *file_name = "test_files/vid_31mb.mp4";
  // char *file_name = "csv_123mb.csv";
  if (!get_bites(&file_bites, file_name)) {
    printf("error in get_bites() func\n");
    return 1;
  }

  printf("Before encoding\n");
  // for (size_t i = 0; i < file_bites.bite_lenght; i++) {
  //   printf("%d\n", file_bites.bites[i]);
  // }
  clock_t start, end;
  double cpu_time_used;

  start = clock();
  encode_assignment5(&file_bites, 128);
  end = clock();
  cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
  printf("Encode time: %.6f seconds\n", cpu_time_used);

  printf("After encoding\n");
  // for (size_t i = 0; i < file_bites.bite_lenght; i++) {
  //   printf("%d\n", file_bites.bites[i]);
  // }
  start = clock();
  decode_assignment5(&file_bites, 128);
  end = clock();
  cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
  printf("Decode time: %.6f seconds\n", cpu_time_used);

  printf("After decoding\n");
  // for (size_t i = 0; i < file_bites.bite_lenght; i++) {
  //   printf("%d\n", file_bites.bites[i]);
  // }

  free(file_bites.bites);
  return 0;
}
