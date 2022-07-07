module top ( y1 , y2 , a , b , c );
input a , b , c ;
output y1 , y2 ;
wire g1 , g2 , g3 ;
wire t_0 ;

nand ( g2 , a , b );
not ( g1 , c );
nand ( g3 , b , g1 );
or ( y1 , g2 , t_0 );
and ( y2 , g3 , g2 );
endmodule