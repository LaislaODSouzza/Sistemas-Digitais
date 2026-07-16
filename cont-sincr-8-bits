// Módulo: counter_8bit
// ==========================
module counter (
    input clock,
    input rst,
    output reg [7:0] count
);

    always @(posedge clock or negedge rst) begin
        if (!rst) begin
            count <= 8'h00; // Reset assíncrono ativo baixo
        end else begin
            count <= count + 1'b1;
        end
    end

endmodule


// Módulo: dec7seg
// ==========================
module dec7seg (
    input [3:0] X,    
    output a, b, c, d, e, f, g 
);

    // Expressões Dataflow a partir do Mapa de Karnaugh
    assign a = (X[1] & ~X[0]) | 
            (~X[2] & ~X[0]) | 
            (~X[3] & X[1]) | 
            (X[2] & X[1]) | 
            (~X[3] & X[2] & X[0]) | 
            (X[3] & ~X[2] & ~X[1]) |
            (~X[1] & ~X[0] & X[3]);
    
    assign b = (~X[3] & ~X[2]) | 
           (~X[2] & ~X[0]) | 
           (~X[3] & X[1] & X[0]) | 
           (~X[3] & ~X[1] & ~X[0]) | 
           (X[3] & ~X[1] & X[0]);

    assign c = (X[3] & ~X[2]) |
            (~X[1] & X[0]) |
            (~X[3] & X[2]) |
            (~X[3] & ~X[1]) |
            (~X[3] & X[0]);
    
    assign d = (~X[1] & ~X[0] & ~X[2]) |
            (~X[1] & ~X[0] & X[3]) |
            (~X[1] & X[0] & X[2]) |
            (X[1] & X[0] & ~X[2]) |
            (X[1] & ~X[0] & ~X[3]) |
            (X[1] & ~X[0] & X[2]);
    
    assign e = (X[1] & ~X[0]) |
            (X[3] & X[2]) |
            (X[3] & X[1]) |
            (~X[2] & ~X[0]);
    
    assign f = (~X[1] & ~X[0]) |
            (X[3] & ~X[2]) |
            (X[3] & X[1]) |
            (~X[3] & X[2] & ~X[1]) |
            (X[1] & ~X[0] & X[2]);

    assign g = (X[1] & ~X[0]) |
            (X[3] & ~X[2]) |
            (X[3] & X[0]) |
            (~X[3] & ~X[2] & X[1]) |
            (~X[3] & X[2] & ~X[1]);

endmodule


// Módulo: top
// ==========================
module top (
    input clk_pit, // Conectado ao botão (btn1) ou ao clock interno (clk_1hz)
    input rst_botao,   // Botão de reset
    output [7:0] leds,
    output a0, b0, c0, d0, e0, f0, g0, // Trabalha com as unidades
    output a1, b1, c1, d1, e1, f1, g1  // Responsável pelas Dezenas
);

    wire [7:0] fio_contagem;

    // Instanciação do contador
    counter meu_contador (
        .clock(clk_pit),
        .rst(~rst_botao),
        .count(fio_contagem)
    );

    // Conexão dos LEDs
    assign leds = fio_contagem;

    // Display 0 - Unidades (Os 4 bits menos significativos)
    dec7seg unidades (
        .X(fio_contagem[3:0]),
        .a(a0), .b(b0), .c(c0), .d(d0), .e(e0), .f(f0), .g(g0)
    );

    // Display 1 - Dezenas (Os 4 bits mais significativos)
    dec7seg dezenas (
        .X(fio_contagem[7:4]),
        .a(a1), .b(b1), .c(c1), .d(d1), .e(e1), .f(f1), .g(g1)
    );

endmodule

//========================================================================
// Pinout e Pinagem

// ========== ENTRADAS ==========
clk_pit = clk_1hz;    // Ou `clk_pit = btn1` para ativar uma unidade no contador manualmente
rst_botao   = btn0;   // Botão 0 (Reset)

// ========== LEDs ==========
leds[0] = led0;
leds[1] = led1;
leds[2] = led2;
leds[3] = led3;
leds[4] = led4;
leds[5] = led5;
leds[6] = led6;
leds[7] = led7;

// ===== DISPLAY DAS UNIDADES =====
a0 = segd0.a_on;
b0 = segd0.b_on;
c0 = segd0.c_on;
d0 = segd0.d_on;
e0 = segd0.e_on;
f0 = segd0.f_on;
g0 = segd0.g_on;

// ====== DISPLAY DAS DEZENAS =====
a1 = segd1.a_on;
b1 = segd1.b_on;
c1 = segd1.c_on;
d1 = segd1.d_on;
e1 = segd1.e_on;
f1 = segd1.f_on;
g1 = segd1.g_on;
