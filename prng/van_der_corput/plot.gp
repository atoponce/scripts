set term png;
set output 'random.png';
#set output 'van_der_corput.png';
set key off;
set term png size 1000,1000;
plot 'random.txt' linetype 1 pointsize .5 linecolor black;
#plot 'sequence.txt' linetype 1 pointsize .5 linecolor black;
