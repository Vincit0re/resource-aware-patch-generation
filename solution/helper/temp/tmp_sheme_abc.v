module patch(t_0, g2, g1);
	output t_0;
	input g2;
	input g1;
	// Target: t_0
	wire term_0;
	or (term_0, g2, g1, 1'b0);
	and (t_0, term_0, 1'b1);
endmodule
