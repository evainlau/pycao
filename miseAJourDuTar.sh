cd $dirpycao/distributed
prefix="pycao/"
tar --transform "s:^:pycao/:" -c  -f pycao.tar *.py *.txt 
mv pycao.tar ..
