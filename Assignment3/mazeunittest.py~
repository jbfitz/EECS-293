import sys
import unittest

from maze import *

class OneCellTestCase(unittest.TestCase):
	def setUp(self):
		self.one_cell = MazeCell()

	def runTest(self):
		self.assertFalse(self.one_cell.valid)
		self.assertRaises(UninitializedObjectException, self.one_cell.passages)
		self.assertRaises(UninitializedObjectException, self.one_cell.connected_cells)


class OneRouteTestCase(unittest.TestCase):
	def setUp(self):
		self.one_route = MazeRoute()

	def runTest(self):
		self.assertFalse(self.one_route.valid)
		self.assertRaises(UninitializedObjectException, self.one_route.travel_time)


	
class TwoCellDeadEndTestCase(unittest.TestCase):
	def setUp(self):
		self.one_cell = MazeCell()
		self.two_cell = MazeCell()
		
		self.one_cell_passages = {self.two_cell:10}
		self.two_cell_passages = {self.one_cell:sys.maxint}
		
		self.one_cell.add_passages(self.one_cell_passages)
		self.two_cell.add_passages(self.two_cell_passages)
		
	def runTest(self):
		self.assertTrue(self.one_cell.valid)
		self.assertTrue(self.two_cell.valid)
		
		self.assertFalse(self.one_cell.is_dead_end())
		self.assertTrue(self.two_cell.is_dead_end())
		
		self.assertEqual(self.one_cell.passages(), self.one_cell_passages)
		self.assertEqual(self.two_cell.passages(), {})

		self.assertEqual(self.one_cell.connected_cells(), [self.two_cell])
		self.assertEqual(self.two_cell.connected_cells(), [])
		
		self.assertEqual(self.one_cell.passage_time_to(self.two_cell), 10)
		self.assertEqual(self.two_cell.passage_time_to(self.one_cell), sys.maxint)

		
class TwoCellConnectedCase(unittest.TestCase):
	def setUp(self):
		self.one_cell = MazeCell()
		self.two_cell = MazeCell()
		
		self.one_cell_passages = {self.two_cell:10}
		self.two_cell_passages = {self.one_cell:5}
		
		self.one_cell.add_passages(self.one_cell_passages)
		self.two_cell.add_passages(self.two_cell_passages)
	       
	def runTest(self):
		self.assertTrue(self.one_cell.valid)
		self.assertTrue(self.two_cell.valid)

		self.assertFalse(self.one_cell.is_dead_end())
		self.assertFalse(self.two_cell.is_dead_end())
		
		self.assertEqual(self.one_cell.passages(), self.one_cell_passages)
		self.assertEqual(self.two_cell.passages(), self.two_cell_passages)

		self.assertEqual(self.one_cell.connected_cells(), [self.two_cell])
		self.assertEqual(self.two_cell.connected_cells(), [self.one_cell])
			       
		self.assertEqual(self.one_cell.passage_time_to(self.two_cell), 10)
		self.assertEqual(self.two_cell.passage_time_to(self.one_cell), 5)

class FourCellTestCase(unittest.TestCase):
	def setUp(self):
		self.cells = []
		cell_zero = MazeCell()
		cell_one = MazeCell()
		cell_two = MazeCell()
		cell_three = MazeCell()
		

		self.cells.append(cell_zero)
		self.cells.append(cell_one)
		self.cells.append(cell_two)
		self.cells.append(cell_three)

		self.cells[0].add_passages({self.cells[1]: 10, self.cells[2]:10, self.cells[3]: sys.maxint})

		self.cells[1].add_passages({self.cells[0]: 5, self.cells[2]: 10, self.cells[3]:15})

		self.cells[2].add_passages({self.cells[0]: 25, self.cells[1]: sys.maxint, self.cells[3]: 5})

		self.cells[3].add_passages({self.cells[0]: sys.maxint, self.cells[1]: sys.maxint, self.cells[2]: sys.maxint})

		self.impossible_route = MazeRoute()
		self.impossible_route.add_cells([self.cells[0], self.cells[3]])

		self.possible_route = MazeRoute()
		self.possible_route.add_cells([self.cells[0], self.cells[1], self.cells[2], self.cells[3]])
		
		self.one_cell_route = MazeRoute()
		self.one_cell_route.add_cells([self.cells[0]])          
		pass

class OneCellRouteTest(FourCellTestCase):
	def runTest(self):
		self.assertTrue(self.one_cell_route.valid)
		self.assertEquals(self.one_cell_route.get_cells(), [self.cells[0]])
		self.assertEquals(self.one_cell_route.travel_time(), 0)
		self.assertEquals(str(self.one_cell_route), str(["End of route"]))
		pass
	

class ImpossibleRouteTest(FourCellTestCase):
	def runTest(self):		
		self.assertTrue(self.impossible_route.valid)
		self.assertEquals(self.impossible_route.get_cells(), [self.cells[0], self.cells[3]])
		self.assertEquals(self.impossible_route.travel_time(), sys.maxint)
		self.assertEquals(str(self.impossible_route), "MazeRoute" + str(hash(self.impossible_route)) + ": No Passage")
		pass
		  
class PossibleRouteCase(FourCellTestCase):
	def runTest(self):
		self.assertTrue(self.possible_route.valid)
		self.assertEquals(self.possible_route.get_cells(), [self.cells[0],self.cells[1],self.cells[2],self.cells[3]])
		self.assertEquals(self.possible_route.travel_time(), 25)
		self.assertEquals(str(self.possible_route), str([
                                                                str(self.cells[0]) + " to " + str(self.cells[1])+ ": " + str(10),
                                                                str(self.cells[1]) + " to " + str(self.cells[2])+ ": " + str(10),
                                                                str(self.cells[2]) + " to " + str(self.cells[3])+ ": " + str(5),
                                                                "End of route"]))
		pass
				  
if __name__ == "__main__":
	unittest.main()
