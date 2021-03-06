"""

File: as3unittest.py

Author: James Fitzpatrick

Date: 9/13/13

"""

import sys

from testify import *

from maze import *

class InvalidTestCase(TestCase):
	@class_setup
	def init_invalid_cell(self):
		self.cell_one = MazeCell()
		self.route_one = MazeRoute()
		self.maze_one = Maze()

	def test_cell_invalid(self):
		assert_equal(self.cell_one.valid, False)
		assert_raises(UninitializedObjectException, self.cell_one.passages)
		assert_raises(UninitializedObjectException, self.cell_one.connected_cells)
	
	def test_route_invalid(self):
		assert_equal(self.route_one.valid, False)
		assert_raises(UninitializedObjectException, self.route_one.travel_time)


	def test_maze_invalid(self):
		assert_equal(self.maze_one.valid, False)
		assert_equal(str(self.maze_one), "Uninitialized Maze")
		assert_raises(UninitializedObjectException, self.maze_one.valid_or_raise)


class TwoCellCase(TestCase):
	@class_setup
	def init_two_cell(self):
		self.cell_one = MazeCell()
		self.cell_two = MazeCell()
		self.route_one = MazeRoute()
		self.route_two = MazeRoute()
		self.maze_one = Maze()

class TwoCellDeadEnd(TwoCellCase):
	@setup
	def init_dead_end(self):
		self.cell_one_passages = {self.cell_two: 10}
		self.cell_two_passages = {self.cell_one: sys.maxint}

		self.cell_one.add_passages(self.cell_one_passages)
		self.cell_two.add_passages(self.cell_two_passages)
		self.route_one.add_cells([self.cell_one, self.cell_two])
		self.route_two.add_cells([self.cell_two, self.cell_one])
		self.maze_one.add_cells([self.cell_one, self.cell_two])

	def test_dead_end_cell(self):
		assert_equal(self.cell_one.valid, True)
		assert_equal(self.cell_two.valid, True)

		assert_equal(self.cell_one.is_dead_end(), False)
		assert_equal(self.cell_two.is_dead_end(), True)
		
		assert_equal(self.cell_one.passages(), self.cell_one_passages)
		assert_equal(self.cell_two.passages(), {})

		assert_equal(self.cell_one.connected_cells(), [self.cell_two])
		assert_equal(self.cell_two.connected_cells(), [])
		
		assert_equal(self.cell_one.passage_time_to(self.cell_two), 10)
		assert_equal(self.cell_two.passage_time_to(self.cell_one), sys.maxint)

	def test_impossible_route(self):
		assert_equals(self.route_two.valid, True)
		assert_equals(self.route_two.get_cells(), [self.cell_two, self.cell_one])
		assert_equals(self.route_two.travel_time(), sys.maxint)
		
	def test_two_cell_maze(self):
		assert_equals(self.maze_one.valid, True)
		assert_equals(self.maze_one.route_first(self.cell_two).get_cells(), [self.cell_two])
		assert_equals(self.maze_one.route_first(self.cell_one).get_cells(), [self.cell_one, self.cell_two])

class TwoCellConnected(TwoCellCase):
	@setup
	def init_two_connected(self):
		self.cell_one_passages = {self.cell_two: 10}
		self.cell_two_passages = {self.cell_one: 5}

		self.cell_one.add_passages(self.cell_one_passages)
		self.cell_two.add_passages(self.cell_two_passages)
		self.route_one.add_cells([self.cell_one, self.cell_two])
		self.maze_one.add_cells([self.cell_one, self.cell_two])

	def test_two_connected_cell(self):
		assert_equal(self.cell_one.valid, True)
		assert_equal(self.cell_two.valid, True)

		assert_equal(self.cell_one.is_dead_end(), False)
		assert_equal(self.cell_two.is_dead_end(), False)
		
		assert_equal(self.cell_one.passages(), self.cell_one_passages)
		assert_equal(self.cell_two.passages(), self.cell_two_passages)

		assert_equal(self.cell_one.connected_cells(), [self.cell_two])
		assert_equal(self.cell_two.connected_cells(), [self.cell_one])
			       
		assert_equal(self.cell_one.passage_time_to(self.cell_two), 10)
		assert_equal(self.cell_two.passage_time_to(self.cell_one), 5)



class FourCellTestCase(TestCase):
	@class_setup
	def four_cell_inits(self):
		self.cells = [MazeCell(), MazeCell(), MazeCell(), MazeCell()]
		self.route = MazeRoute()
		self.maze = Maze()


class FourCellValidTestCase(FourCellTestCase):
	@setup
	def build_maze(self):
		self.cells[0].add_passages({self.cells[1]: 10, self.cells[2]: 20})
		self.cells[1].add_passages({self.cells[2]: 5, self.cells[3]: 40})
		self.cells[2].add_passages({self.cells[3]: 5, self.cells[0]: 80})
		self.cells[3].add_passages({self.cells[0]:0})

		self.route.add_cells(self.cells)

		self.maze.add_cells(self.cells)
		self.first_route = self.maze.route_first(self.cells[0])


	def test_four_route(self):
		assert_equals(self.route.travel_time(), 20)
		pass

	def test_four_maze(self):
		assert_equals(self.first_route.valid, True)
		assert_gt(len(self.first_route.get_cells()), 1)
		pass

class FourCellOutsideMazeCase(FourCellTestCase):
	@setup
	def build_maze(self):
		self.cells[0].add_passages({self.cells[1]: 10, self.cells[2]: 20})
		self.cells[1].add_passages({self.cells[2]: 5, self.cells[3]: 40})
		self.cells[2].add_passages({self.cells[3]: 5, self.cells[0]: 80})
		self.cells[3].add_passages({self.cells[0]:0})

		self.maze.add_cells([self.cells[3], self.cells[0]])
		self.first_route = self.maze.route_first(self.cells[3])


	def test_four_maze(self):
		assert_equals(self.first_route.valid, True)
		assert_equals(len(self.first_route.get_cells()), 0)
		assert_raises(UninitializedObjectException, self.first_route.travel_time)
		pass




if __name__ == "__main__":
	run()
