module top (n13173, n4646, n10291, n13049, n10292, t_0);
   input n13173, n4646, n10291, n13049, n10292;
   output t_0;
   wire mod_n10, mod_n11, mod_n12, mod_n13, mod_n14, mod_n15, mod_n16, mod_n17, mod_n18, mod_n19, mod_n20, mod_n21, mod_n22, mod_n23, mod_n24, mod_n25, mod_n26, mod_n27, mod_n7, mod_n8, mod_n9;
   not (mod_n10, n10292);
   nand (mod_n11, mod_n9, mod_n8, mod_n7, mod_n10, n13049);
   nand (mod_n12, mod_n9, n4646, mod_n7, mod_n10, n13049);
   nand (mod_n13, mod_n9, mod_n8, mod_n7, n10292, n13049);
   not (mod_n14, n13049);
   nand (mod_n15, mod_n9, n4646, n13173, mod_n10, mod_n14);
   nand (mod_n16, n10291, n4646, n13173, n13049);
   nand (mod_n17, mod_n13, mod_n12, mod_n11, mod_n16, mod_n15);
   nand (mod_n18, mod_n9, n4646, n13173, n10292, mod_n14);
   nand (mod_n19, n10291, mod_n8, mod_n7, n10292, n13049);
   nand (mod_n20, n10291, n4646, n13173, mod_n10, mod_n14);
   nand (mod_n21, n10291, mod_n8, mod_n7, mod_n10, n13049);
   nand (mod_n22, mod_n20, mod_n19, mod_n18, mod_n21);
   nand (mod_n23, n10291, mod_n8, n13173, mod_n10, mod_n14);
   nand (mod_n24, n10291, n4646, mod_n7, n10292, mod_n14);
   nand (mod_n25, mod_n9, n4646, mod_n7, n10292, n13049);
   nand (mod_n26, n10291, mod_n8, n13173, n10292, mod_n14);
   nand (mod_n27, mod_n25, mod_n24, mod_n23, mod_n26);
   not (mod_n7, n13173);
   not (mod_n8, n4646);
   not (mod_n9, n10291);
   nor (t_0, mod_n27, mod_n22, mod_n17);
endmodule