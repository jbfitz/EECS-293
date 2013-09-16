"""
Module: Maze

Author: James Fitzpatrick

Date: 9/9/13

"""

import copy
import random
import sys

			
class UninitializedObjectException(ValueError):
	"""
	An error raised when an object isn't initialized.
    
	In our current sense, this means that a cell has not
	been connected to any other cell, even if that connection 
	is impassible
	"""
	pass
		
		
class MazeCell(object):
	"""
	This object represents a room within the maze.
	"""

	def __init__(self):
		self._connections = {}
		self.valid = False
	
	def __hash__(self):
		return id(self)
		
	def __str__(self):
		return "MazeCell" + str(hash(self))
		
	def valid_or_raise(self):
		"""
		Checks to see if this cell is valid. 
		Raise a UninitializedObjectException if this cell is not valid
		"""
		if not self.valid: raise UninitializedObjectException()
	
	def add_passages(self, passages):
		"""
		Adds a list of passages to this cell
		This object is immutable once the passages are set
		"""
		
		# If we have already been set valid, don't add more paths
		if self.valid:
			return False
		
		# Add the valid contents of the map to our existing set of passages
		self._connections = copy.copy(passages)
		self.valid = True
				
		return True
	
	def passages(self):
		"""
		Returns the passages of the MazeRoute. 
	
		Raises UninitializedObjectException if the cell is invalid.
		"""
		
		self.valid_or_raise()

		reachablePassages = {key: value for key, value in self._connections.iteritems()
					if value != sys.maxint}
		
		return copy.copy(reachablePassages)
		
		
	def passage_time_to(self, cell):
		"""
		Return the time to go from this cell to another cell through 
		its connections. 

		If a cell is not currently connected, or unable to be reached, 
		this will return sys.maxint. 

		Raises UninitializedObjectException if this cell is currently invalid. 
		"""
		self.valid_or_raise()
			   
		return self._connections.get(cell, sys.maxint)
		
	def connected_cells(self):
		"""Returns a list of all the cells connected to this one"""
		self.valid_or_raise()
		
		con_cells = []

		for cell in self._connections:
			if self._connections[cell] == sys.maxint:
				pass
			else:
				con_cells.append(cell)
		return con_cells
		
	def is_dead_end(self):
		"""Looks to see if any moves from this cell are possible"""
		connected_cells = self.connected_cells()
		
		if len(connected_cells) == 0:
			return True
		else:
			return False

			       
class MazeRoute(object):
	"""Represents a path, in order, of traversing several MazeCells"""
	
	def __init__(self):
		self.valid = False
		self._cells = []
		pass
		
		
				
	def __str__(self):
		self.valid_or_raise()

		if self.travel_time() == sys.maxint:
			return "MazeRoute" + str(hash(self)) + ": No Passage"
			
		route_list = []
			
		for index in range(len(self._cells)):
			if index != len(self._cells) - 1:
				route_list.append(str(self._cells[index]) + " to " + 
					str(self._cells[index+1]) + ": " + 
					str(self._cells[index].passage_time_to(self._cells[index+1])))
			else:
				route_list.append("End of route")
				
		
		return str(route_list)
		
		
		
	def valid_or_raise(self):
		"""
		Checks to see if route cell is valid. 
		Raise a UninitializedObjectException if this route is not valid
		"""
		if not self.valid: raise UninitializedObjectException()

		
	def add_cells(self, route):
		"""
		Creates or appends a list representing a route of cells from first to last
		Takes a list of cells as input
		"""
	
		if self.valid:
			return False

		if any(not cell.valid for cell in route):
			raise UnintializedObjectException()
		
		self._cells = copy.copy(route)
		self.valid = True
		return True
		
	def get_cells(self):
		"""
		Returns the list of cells in the route in order
		Returns the list regardless of whether or not the route is passible
		Raise a UninitializedObjectException if any cells are invalid
		"""
		if any(not cell.valid for cell in self._cells):
			raise UnintializedObjectException()
				
		return copy.copy(self._cells)
			
	def travel_time(self):
		"""
		Returns the total time to travel from the first cell in the route to the last
		Returns sys.maxint if the route is not possible
		Returns 0 if there is only one cell in the route
		"""
		self.valid_or_raise()
		
		if any(not cell.valid for cell in self._cells):
			raise UninitializedObjectException()
		
		if len(self._cells) == 1:
			return 0
			
		if len(self._cells) == 0:
			# Since our maze returns an empty list if the maze route
			# Leaves the maze, I decided that a route of no cells is
			# Invalid as a cellless route makes no sense
			raise UninitializedObjectException()

		travel_time = 0
		
		for index in range(len(self._cells)-1):
			if self._cells[index].passage_time_to(self._cells[index+1]) != sys.maxint:
				travel_time += self._cells[index].passage_time_to(self._cells[index+1]) 
			else:
				return sys.maxint
		
		return travel_time
			


class Maze(object):
	"""
	A representation of a maze, a collection of cells that are all connected
	Cells are not stored in any particular order
	"""
	def __init__(self):
		self.valid = False
		self._cells = []
		pass

	def __str__(self):
		if not self.valid:
			return "Uninitialized Maze"

		strfrm = ""

		for cell in self._cells:
			if not cell.valid:
				raise UninitializedObjectexception()			

			strfrm = strfrm + "\n" + str(cell)
		
			if len(cell.passages()) == 0:
				strfrm + "\n\tNo passages"

			for dest, time in cell.passages().iteritems():
				strfrm + "\n\t" + str(dest) + ": " + str(time)
				
		return strfrm
	
	def add_cells(self, cells):
		"""
		Takes a iterable collection of cells

		Returns false and does not change the maze's cells if already set
		Otherwise, sets the mazes _cells to a copy of the input

		Raises UintializedObjectException if any of the inputed cells are invalid
		"""
		if self.valid:
			return False
		
		if any(not cell.valid for cell in cells):
			raise UninitializedObjectExcption()

		self._cells = copy.copy(cells)
		self.valid = True
		return True

	def route_first(self, initial_cell):
		"""
		Starting from the initial input, randomly explores the maze 
		until a dead end, exit, or loop is encountered

		Returns an empty list if a valid cell outside of the maze is encountered.

		Raises a UnitializedObjectException if either the maze or the cells 
		along the path are invalid
		"""
		self.valid_or_raise()

		current_cell = initial_cell
		visited_cells = []
		return_route = MazeRoute()

		while True:
			current_cell.valid_or_raise()

			if not current_cell in self._cells:
				return_route.add_cells([])
				break
			
			if current_cell in visited_cells:
				# We stil want this cell to be in the route
				# Although a loop kay present problems in 
				# the future, the first lap is still a route
				visited_cells.append(current_cell)
				return_route.add_cells(visited_cells)
				break
	

			# This line must be after the already visited check
			# to avoid a tautology
			visited_cells.append(current_cell)

			if current_cell.is_dead_end():
				return_route.add_cells(visited_cells)
				break
			
			current_cell = current_cell.connected_cells()[0]
			#random.choice(current_cell.connected_cells())

		return return_route

			
	def valid_or_raise(self):
		"""
		Checks to see if maze is valid. 
		Raise a UninitializedObjectException if this route is not valid
		"""
		if not self.valid: raise UninitializedObjectException()


