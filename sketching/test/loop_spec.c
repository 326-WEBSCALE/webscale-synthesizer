done=0;
repeat i : 4 {
	if(done == 3){
		skip
	}
	else{
		x = x<<1;
		done = done + 1;
	}
}
