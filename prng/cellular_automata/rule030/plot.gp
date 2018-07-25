set term png;
set output 'plot.png';
set key off;
set term png size 1000,1000;
plot 'sequence.txt' linetype 1 pointsize .5 linecolor black;
