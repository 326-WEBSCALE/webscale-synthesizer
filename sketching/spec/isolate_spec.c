r = 0;
done = 0;
repeat i : 4 {
  if ((done == 0) and (not (x & (1 << i) == 0))) {
    done = 1;
    r = 1 << i;
  }
}
done = 1;