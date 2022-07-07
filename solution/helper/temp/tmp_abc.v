// Benchmark "patch" written by ABC on Tue Jul 05 22:49:52 2022

module patch ( 
    g2, g1,
    t_0  );
  input  g2, g1;
  output t_0;
  or2    g0(.a(g1), .b(g2), .O(t_0));
endmodule


