# Lab-Sistemas-Digitais: Contador Síncrono de 8 Bits com Decodificação Hexadecimal para Displays de 7 Segmentos
Código em Verilog feito nas aulas de laboratório da matéria de Sistemas Digitais pela Universidade Federal de Sergipe (UFS).

## 1. Descrição do Projeto
Este repositório é voltado para o desenvolvimento, a síntese lógica e a validação experimental de um **contador síncrono binário de 8 bits**, modelado em linguagem de descrição de hardware **Verilog**. O sistema computa estímulos temporais externos (clock) e mapeia dinamicamente o valor acumulado em duas interfaces de saída concorrentes: um barramento de 8 LEDs e dois displays de 7 segmentos (unidades e dezenas), utilizando a representação alfanumérica do sistema **hexadecimal** (`0` a `F`).

O circuito foi projetado e validado somente por meio do ecossistema de prototipagem virtual da placa **Pitanga**, com o objetivo de cumprir os requisitos teóricos e práticos das Atividades 00 e 01.

---

## 2. Arquitetura e Modularidade do Hardware

O sistema foi estruturado de forma modular, dividindo-se em três blocos funcionais interdependentes:

* **`counter`**: Bloco sequencial estruturado em nível de transferência entre registradores (RTL). Realiza o incremento da palavra de 8 bits a cada borda de subida do sinal de clock (`posedge clock`). Incorpora uma rotina de reset assíncrono ativo em nível lógico baixo (`negedge rst`), que força o registrador instantaneamente ao vetor nulo (`8'h00`).
* **`dec7seg`**: Bloco combinacional baseado em modelagem por fluxo de dados (*dataflow*). Traduz os vetores de 4 bits gerados pelo contador em sinais para os segmentos catódicos/anódicos, mapeando corretamente os caracteres de `0` a `9` e as letras de `A` a `F`.
* **`top`**: Módulo estrutural de nível superior (*Top-Level*). Instancia os submódulos, gerencia o barramento de interconexão interna e aplica uma inversão lógica no terminal de reset (`~rst_botao`) para compatibilizar a reatividade do código com o comportamento elétrico padrão dos botões físicos da plataforma Pitanga.

---

## 3. Análise Comparativa das Variações de Clock (Mapeamento de Pinos)

O circuito foi submetido a duas abordagens distintas de estímulo temporal no arquivo de mapeamento físico de terminais (`pitanga.pinout`):

### Variação A: Estímulo por Botão Manual (`clk_pit = btn1`)
* **Mapeamento de Pinos**: O clock do contador é ligado diretamente para o terminal físico do botão `btn1`.
* **Dinâmica do Hardware**: O incremento do acumulador ocorre de maneira assíncrona em relação ao tempo real, reagindo exclusivamente aos eventos mecânicos. Cada pressionamento do usuário força uma borda de subida (`posedge`), avançando o estado interno do contador em exatamente uma unidade.
* **Comportamento Prático**: Permite verificar de forma controlada a transição bit a bit do barramento de LEDs e inspecionar as curvas lógica do decodificador `dec7seg` em caracteres críticos (como a transição de `09` para `0A`).

### Variação B: Estímulo por Clock Interno (`clk_pit = clk_1hz`)
* **Mapeamento de Pinos**: O clock é desvinculado do botão e conectada ao gerador de base de tempo nativo da placa (`clk_1hz`).
* **Dinâmica do Hardware**: O sistema passa a operar sob um regime de varredura cíclica contínua, governado por uma onda quadrada periódica de frequência controlada de 1 Hz (período de 1 segundo). 
* **Comportamento Prático**: O contador executa uma progressão autônoma, percorrendo o espectro numérico completo de `00` a `FF` (0 a 255 em decimal) sem necessidade de interação humana.

---

## 4. Relatório de Síntese Lógica e Métricas

A compilação e o mapeamento tecnológico do circuito na arquitetura alvo geraram as seguintes métricas de consumo de células lógicas e transistores:

```text
                     DESIGN SUMMARY REPORT
  module     : top
  design file: pitanga.v
  pinout file: pitanga.pinout

  Total number of wires: 107
  Total number of cells: 105
  Total number of ports: 26

  Cell      Instances   Cell      Instances   Cell      Instances
 -----------------------------------------------------------------
  AND2              1 | NAND2            45 | XOR2              0 
  AND3              0 | NAND3             8 | XOR3              0
  AND4              0 | NAND4             3 | XOR4              0
  OR2               7 | NOR2             14 | XNOR2             7
  OR3               3 | NOR3              0 | XNOR3             0
  OR4               0 | NOR4              0 | XNOR4             0
 -----------------------------------------------------------------
  BUF               0 | INV               9 | DFFRSE            8

  Cells utilization: 105
  Transistor count : 786/10000 transistors (7.86 %)
```

### Análise dos Resultados
* **Elementos de Armazenamento**: A alocação exata de 8 instâncias da primitiva sequencial `DFFRSE` (Flip-Flops Tipo D com propriedades de Set/Reset, localizado no lado inferior direito da tabela) comprova a correta inferência do registrador de deslocamento de 8 bits projetado em nível comportamental.
* **Mapeamento de Células Lógicas**: O arranjo combinacional exibe uma predominância das portas universais `NAND2` (45) e `NOR2` (14). Isso evidencia o algoritmo de síntese otimizando e simplificando as expressões booleanas originais em estruturas semicondutoras de eficiência de área.
* **Consumo de Hardware**: O circuito completo demandou apenas **7,86%** da matriz de transistores disponível no chip simulado da placa Pitanga, atestando uma implementação compacta e otimizada para sistemas digitais embarcados de baixo consumo.

*Desenvolvido por Laísla Souza.*
