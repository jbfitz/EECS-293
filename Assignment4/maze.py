"""
Module: Maze

Author: James Fitzpatrick

Date: 9/9/13

"""

import copy
import random
import sys
	
MAX_VALUE = sys.maxint

class UninitializedObjectException(ValueError):
	"""An error raised when an object isn't initialized."""
	pass

class Enum(set):
	"""Enum implementation courtesy of shahjapan"""
	def __getattr__(self, name):
        	if name in self:
        		return name
        	raise AttributeError

Status = Enum(["OK", "ALREADY_VALID", "INVALID_TIME"])

class MazeCell(object):
	"""This object represents a room within the maze."""

	def __init__(self):
		self._connections = {}
		self.valid = False
		self.status = Status.OK
			
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
			self.status = Status.ALREADY_VALID
			return False		
		# If any of the cells contain invalid paths, return false
		if any(value <= 0 for value in passages.values()):
			self.status = Status.INVALID_TIME
			return False
		# Add the valid contents of the map to our existing set of passages
		self._connections = copy.copy(passages)
		self.valid = True
		self.status = Status.OK			
		return True
	
	def passages(self):
		"""
		Returns the passages of the MazeRoute. 
	
		Raises UninitializedObjectException if the cell is invalid.
		"""
		self.valid_or_raise()
		reachablePassages = {key: value for key, value in self._connections.iteritems()
					if value != MAX_VALUE}
		return copy.copy(reachablePassages)
		
	def passage_time_to(self, cell):
		"""
		Return the time to go from this cell to another cell through 
		its connections. 

		If a cell is not currently connected, or unable to be reached, 
		this will return MAX_VALUE. 

		Raises UninitializedObjectException if this cell is currently invalid. 
		"""
		self.valid_or_raise()	   
		return self._connections.get(cell, MAX_VALUE)
		
	def connected_cells(self):
		"""Returns a list of all the cells connected to this one"""
		self.valid_or_raise()
		con_cells = [cell for cell in self._connections if self._connections[cell] != MAX_VALUE]
		return copy.copy(con_cells)
		
	def is_dead_end(self):
		"""Looks to see if any moves from this cell are possible"""		
		return len(self.connected_cells()) == 0

			       
class MazeRoute(object):
	"""Represents a path, in order, of traversing several MazeCells"""
	def __init__(self):
		self.valid = False
		self._cells = []
			
	def __str__(self):
		self.valid_or_raise()
		if self.travel_time() == MAX_VALUE:
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
			raise UninitializedObjectException()
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
		The route is guaranteed to return the travel time between each of the cells at 
		each step		

		Returns MAX_VALUE if the route is not possible
		Returns 0 if there is only one cell in the route
		"""
		return self._travel_calc(self._travel_method_default)

	def _travel_method_default(self, current_cell, destination_cell):
		return current_cell.passage_time_to(destination_cell)		

	def travel_time_random(self):
		"""
		Returns the total time to travel from the first cell in the route to the last
		At each step, the value along the passage is between 1 and the value between
		each of the cells. 

		Returns MAX_VALUE if the route is not possible
		Returns 0 if there is only one cell in the route
		"""
		return self._travel_calc(self._travel_method_random)

	def _travel_method_random(self, current_cell, destination_cell):
		return random.randint(1, current_cell.passage_time_to(destination_cell))

	def _travel_calc(self, calc_method):
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
			if self._cells[index].passage_time_to(self._cells[index+1]) != MAX_VALUE:
				travel_time += calc_method(self._cells[index], self._cells[index+1])
			else:
				return MAX_VALUE
		return travel_time

class Maze(object):
	"""
	A representation of a maze, a collection of cells that are all connected
	Cells are not stored in any particular order
	"""
	def __init__(self):
		self.valid = False
		self._cells = set()
		pass

	def __str__(self):
		if not self.valid:
			return "Uninitialized Maze"
		strfrm = ""
		for cell in self._cells:
			if not cell.valid:
				raise UninitializedObjectException()			

			strfrm = strfrm + "\n" + str(cell)
		
			if len(cell.passages()) == 0:
				strfrm = strfrm + "\n\tNo passages"

			for dest, time in cell.passages().iteritems():
				strfrm = strfrm + "\n\t" + str(dest) + ": " + str(time)	
		return strfrm

	def valid_or_raise(self):
		"""
		Checks to see if maze is valid. 

		Raise a UninitializedObjectException if this route is not valid
		"""
		if not self.valid: raise UninitializedObjectException()
	
	def add_cells(self, cells):
		"""
		Takes a set of cells

		Returns false and does not change the maze's cells if already set
		Otherwise, sets the mazes _cells to a copy of the input

		Raises UintializedObjectException if any of the inputed cells are invalid
		"""
		if self.valid:
			return False
		if any(not cell.valid for cell in cells):
			raise UninitializedObjectException()
		self._cells = set(copy.copy(cells))
		self.valid = True
		return True

	def grab_first(self, cell_list):
		return cell_list[0]

	def route_random(self, initial_cell):
		"""Returns the route from the initial cell by following a random passage"""
		return self._find_route(initial_cell, random.choice)

	def route_first(self, initial_cell):
		"""Returns the route from the initial cell by taking the first available passage"""
		return self._find_route(initial_cell, self.grab_first)

	def _find_route(self, initial_cell, next_cell_method):
		"""
		Starting from the initial input, randomly explores the maze 
		until a dead end, exit, or loop is encountered

		Returns an empty list if a valid cell outside of the maze is encountered.

		Raises a UnitializedObjectException if either the maze or the cells 
		along the path are invalid
		"""
		self.valid_or_raise()
		visited_cells = []
		return self._recursive_routing(initial_cell, visited_cells, next_cell_method)


	def _recursive_routing(self, current_cell, visited_cells, next_cell_method):
		"""
		Recursively checks cells until a dead end or a recurring cell appears in the visited list

		If current cell is not in the maze or not valid, return a route containing []

		Uses passed in method to determine next cell to examine
		"""
		if not current_cell in self._cells or not current_cell.valid:
			return_route = MazeRoute()
			return_route.add_cells([])
			return return_route
		if current_cell in visited_cells:
			visited_cells.append(current_cell)
			return_route = MazeRoute()
			return_route.add_cells(visited_cells)
			return return_route
		
		visited_cells.append(current_cell)
		if current_cell.is_dead_end():
			return_route = MazeRoute()
			return_route.add_cells(visited_cells)
			return return_route
		return self._recursive_routing(next_cell_method(current_cell.connected_cells()),
								visited_cells, next_cell_method)
		

