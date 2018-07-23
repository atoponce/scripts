set term png;
#set output 'halton.png';
set output 'random.png';
set key off;
set term png size 1000,1000;
#plot 'sequence.txt' linetype 1 pointsize .5 linecolor black;
plot 'random.txt' linetype 1 pointsize .5 linecolor black;
