done = 0;
repeat i : 4 {
  if (done == 0 and (x & (1 << i) == 0)) {
    x = x | (1 << i);
  }
  else {
    done = 1;
  }
}
done = 1;