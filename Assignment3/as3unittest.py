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


"""

class TwoCellCase(TestCase):
	@class_setup
	def init_two_cell(self):
		self.cells = [MazeCell(), MazeCell()]
		self.routes = [MazeRoute(), MazeRoute()]
		self.maze_one = Maze()

class TwoCellDeadEnd(TwoCellCase):
	@setup
	def init_dead_end(self)
		self.cell_one_passages = {self.cell_two, 10}
		self.cell_two_passages = {self.cell_one, sys.maxint}

		self.cell_one.add_passages(self.cell_one_passages)
		self.cell_two.add_passages(self.cell_two_passages)
		self.route_one.add_cells([self.cell_one, self.cell_two])
		self.maze_one.add_cells([self.cell_one, self.cell_two])

	

class TwoCellConnected(TwoCellCase):
	@setup
	def init_dead_end(self)
		self.cell_one.add_passages({self.cell_two, 10})
		self.cell_two.add_passages({self.cell_one, 5})
		self.route_one.add_cells([self.cell_one, self.cell_two])
		self.maze_one.add_cells([self.cell_one, self.cell_two])
"""

if __name__ == "__main__":
	run()
