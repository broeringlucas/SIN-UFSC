package Kojun

// baixar o compilador de scala
// entrar na pasta do t2.scala e rodar sbt 
// depois rodar run

object KojunSolucionar extends App {

  // Function to validate a move at a given position
  def movimentoValido(grid: Array[Array[Int]], regioes: Array[Array[Int]], linha: Int, col: Int, k: Int): Boolean = {
    val regiao = regioes(linha)(col)
    val regiaoValida = valoresRegiao(grid, regioes, regiao)
    val validarVizinhos = valoresVizinhos(grid, linha, col)
    val validaAcima = acimaValido(grid, regioes, linha, col, k)
    val validaAbaixo = abaixoValido(grid, regioes, linha, col, k)
    val menorQueRegiao = k <= regiaoValida.length

    !regiaoValida.contains(k) && !validarVizinhos.contains(k) && validaAcima && validaAbaixo && menorQueRegiao
  }

  // Function to check if the upper neighbor is valid
  def acimaValido(grid: Array[Array[Int]], regioes: Array[Array[Int]], linha: Int, col: Int, k: Int): Boolean = {
    linha == (grid.length - 1) || regioes(linha + 1)(col) != regioes(linha)(col) || grid(linha + 1)(col) < k
  }

    // Function to get values in the same region
  def valoresRegiao(grid: Array[Array[Int]], regioes: Array[Array[Int]], regiao: Int): List[Int] = {
    (for {
      i <- grid.indices
      j <- grid(i).indices
      if regioes(i)(j) == regiao
    } yield grid(i)(j)).toList
  }

  // Function to get values of neighboring cells
  def valoresVizinhos(grid: Array[Array[Int]], linha: Int, col: Int): List[Int] = {
    val vizinhos = List(
      (linha + 1, col),
      (linha - 1, col),
      (linha, col + 1),
      (linha, col - 1)
    )

    vizinhos.filter { case (i, j) =>
      i >= 0 && i < grid.length && j >= 0 && j < grid(i).length
    }.map { case (i, j) => grid(i)(j) }
  }

  // Function to check if the lower neighbor is valid
  def abaixoValido(grid: Array[Array[Int]], regioes: Array[Array[Int]], linha: Int, col: Int, k: Int): Boolean = {
    linha == 0 || regioes(linha - 1)(col) != regioes(linha)(col) || grid(linha - 1)(col) > k
  }

    // Function to try placing values at a cell
  def tentarPosicionar(grid: Array[Array[Int]], regioes: Array[Array[Int]], linha: Int, col: Int, ks: List[Int]): Option[Array[Array[Int]]] = {
    val novoGrid = grid.map(_.clone) // Create a new copy of the grid
    if (ks.isEmpty) None // Base case: no more values to try, return None
    else {
      if (movimentoValido(grid, regioes, linha, col, ks.head)) { // Check if placing the value is valid
        novoGrid(linha)(col) = ks.head // Place the value
        solucionar(novoGrid, regioes, linha, col + 1) match { // Recur for next cell
          case Some(solution) => Some(solution) // If solution found, return it
          case None => tentarPosicionar(grid, regioes, linha, col, ks.tail) // Otherwise, try next value
        }
      } else {
        tentarPosicionar(grid, regioes, linha, col, ks.tail) // If move not valid, try next value
      }
    }
  }
  
  // Main solving function
  def solucionar(grid: Array[Array[Int]], regioes: Array[Array[Int]], linha: Int, col: Int): Option[Array[Array[Int]]] = {
    if (linha == grid.length) Some(grid) // Base case: if reached end of linhas, solution found
    else if (col == grid(linha).length) solucionar(grid, regioes, linha + 1, 0) // Move to next linha
    else if (grid(linha)(col) != 0) solucionar(grid, regioes, linha, col + 1) // Cell already filled, move to next cell
    else {
      val kValues = (1 to grid.length).toList // List of possible values to try
      tentarPosicionar(grid, regioes, linha, col, kValues) // Try placing values at current cell
    }
  }


  // Grid represeting values
  val valores10x10 = Array(
    Array(4,0,7,0,4,6,3,0,2,3),
    Array(0,0,0,1,0,4,0,2,0,2),
    Array(2,0,0,4,0,0,7,0,0,4),
    Array(0,6,0,0,0,6,0,4,0,3),
    Array(5,0,5,0,4,0,6,0,0,1),
    Array(4,1,0,3,0,4,2,0,0,0),
    Array(0,0,1,0,0,7,0,3,0,7),
    Array(5,3,0,5,6,0,5,0,6,3),
    Array(3,0,4,0,0,0,0,0,0,0),
    Array(1,0,6,4,3,0,2,0,4,0)
  )

  // Grid representing regions
  val regioes10x10 = Array(
    Array(1,1,2,2,2,2,2,3,3,3),
    Array(1,1,4,2,2,5,5,5,6,6),
    Array(7,7,4,8,8,5,9,9,9,10),
    Array(7,12,12,13,8,8,8,9,11,10),
    Array(12,12,13,13,13,8,9,9,10,10),
    Array(12,12,13,14,14,14,9,15,15,15),
    Array(16,16,14,14,14,17,17,17,15,18),
    Array(19,16,20,20,20,17,17,17,18,18),
    Array(19,16,16,20,20,21,17,22,18,18),
    Array(19,19,19,19,20,21,21,22,18,18),
  )

  // Function to print the grid
  def printGrid(grid: Array[Array[Int]]): Unit = {
    grid.foreach(linha => println(linha.mkString(" ")))
  }

  // Try to solve the grid and print the solution or a message if no solution found
  solucionar(valores10x10, regioes10x10, 0, 0) match {
    case Some(gridSolucionado) =>
      println("Solution found:")
      printGrid(gridSolucionado) // Print the solucionard grid
    case None =>
      println("No solution found.") // No solution found
  }
}
