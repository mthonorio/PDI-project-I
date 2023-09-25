# Filtros e Correlação de Processamento e Digitalização de Imagem

Este projeto foi desenvolvido com técnicas de filtros e correlação de imagens para a disciplina de Processamento e Digitalização de Imagem do semestre 2022.2 ministrada pelo professor Leonardo Vidal Batista.

## Especificação do projeto

Desenvolva, em uma linguagem de programação de sua escolha, um sistema para abrir,
exibir, manipular e salvar imagens RGB com 24 bits/pixel (8 bits/componente/pixel). Não
use bibliotecas ou funções especiais de processamento de imagens. O sistema deve ter a
seguinte funcionalidade:

1. Conversão RGB-HSB-RGB (cuidado com os limites de R, G e B na volta!).
2. Alteração de matiz e saturação no HSB, com posterior conversão a RGB.
3. Negativo. Duas formas de aplicação devem ser testadas: em RGB (banda a banda) e
   na banda B, com posterior conversão para RGB.
4. Correlação m x n com stride (passo), sem nenhum tipo de extensão, sobre R, G e B, filtro definidos em um arquivo (txt) à parte. Testar com filtros Box, Sobel e explicar os resultados. Compare Box15x1(Box1x15(Image)) com Box(15x15), em termos de resultado e tempo de processamento. Para o Sobel, aplique expansão de histograma para [0, 255]. Para o filtro de Sobel, aplique valor absoluto ao resultado da correlação, seguido por expansão de histograma.


## Módulos

- **get_negative_pixels**: Captura todos os pixels da imagem, separa suas cores em listas e converte subtraindo o valor 255 do valor de cada cor, ou seja, faz a subtração para o (Red, Green and Blue) da imagem e retorna o resultado em uma lista de listas.
- **turn_negative**: Chama a função (get_negative_pixels), itera transformando os pixels retornados em imagem e retorna a imagem.
- **rgb_to_hsb**: Recebe uma imagem RGB e cria os ajustes necessários para converter os pixels para HSB utilizando uma fórmula correta para isso. O retorno da função é uma lista de listas, sendo uma lista para H, uma para S e outra para B. 
- **get_rpg_pixels_from_hsb**: Recebe a lista de listas da função rgb_to_hsb no formato de HSB, converte e retorna em formato RGB.
- **hsb_to_rgb**: Recebe uma lista de listas de uma lista do tipo float como parâmetro e retorna um objeto do tipo Image. Por fim, também é o responsável por rotacionar a imagem à sua posição original. 
- **negative_on_b**: Chama a função de RGB to HSB para a imagem e aplica o negativo no B e retorna a imagem em RGB novamente.
- **call_correlation_mxn**: Valida se os valores passados de m x n são validos, caso sejam, passa os parâmetros e retorna a função de correlational.
- **correlational**: Aplica o filtro de correlação na imagem através da manipulação de pixels utilizando a numpy e retorna uma imagem.
- **histogram_expansion**: Aumenta o contraste da imagem somente após a mesma utilizar o filtro de Sobel.  
- **read_correlational_filters**: Função que ler todos os arquivos TXT da pasta de testes com os parâmetros de filtros escritos e seus devidos offsets, trata os dados dos filtros, aplica na imagem cada filtro pixel a pixel e retorna uma imagem.

## Execução

Para a execução do projeto basta executar no terminal:

```
python main.py
```

## Colaboradores

| <a href="https://www.linkedin.com/in/matheushonorio" target="_blank">**Matheus Honório**</a> |                                                  <a href="https://www.linkedin.com/in/victoria-monteiro-pontes/" target="_blank">**Victoria Monteiro**</a>                                                   |
|  :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :-:
|              <img src="https://avatars.githubusercontent.com/u/52137826?v=4" width="200px"> </img>     | <img src="https://avatars.githubusercontent.com/u/52867523?v=4" width="200px"> </img> | 
|           <a href="https://github.com/mthonorio" target="_blank">`github.com/MatheusHonorio`</a>    |                                                            <a href="https://github.com/vmp309" target="_blank">`github.com/VictoriaMonteiro`</a>                                                             |     |
