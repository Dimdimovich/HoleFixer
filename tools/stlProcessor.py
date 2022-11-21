from typing import Dict, Any, Union

import numpy as np
from stl import mesh, Mesh
import vtkplotlib as vpl
import pymeshfix


class STLProcessor:
    """
    Processor which try to fix holes and plot results.
    It uses pymeshfix lib to generate reference fixed object.

    :param string filename: full name of the importing stl mesh

    :ivar mesh.Mesh stl_mesh: Mesh object for keeping the processed stl
    :ivar list holes: list of holes where each hole is a list of 3D tuples - points
    :ivar dict hole_edges: dictionary with edges appearing only in one triangle. Tuple of two 3D tuples is a key.
                    Triangle index is a value
    :ivar dict mesh_points_dict: dictionary with unique points in form of 3D tuples as keys. Values are lists of 2D
                    tuples where the 1st value is a number of a triangle with this point, the 2nd value is int position
                    in this triangle
    :ivar dict mesh_edges_dict: dictionary with edges arranged as tuples with two edge points. Values are indices of
                                triangles including these edges
    :ivar list holes_unique_points: list of unique points

    """
    def __init__(self, filename=None):
        # parameter declaration and dummy initialization
        self.stl_mesh = None
        self.holes = []
        self.hole_edges = {}
        self.mesh_points_dict = {}
        self.mesh_edges_dict = {}
        self.holes_unique_points = []

        # preform processing if filename is provided
        if filename is not None:
            self.filename = filename
            print()
            print("Mesh hole fixing started. File name:", filename)
            # create stl mesh with normals preserved
            self.stl_mesh = mesh.Mesh.from_file(self.filename, calculate_normals=False)
            # initialize point and edge dictionaries
            self.fill_mesh_dicts()
            self.process_mesh()

    def process_mesh(self):
        self.create_ref_mesh()
        # colorize holes of the initial mesh
        self.find_holes()
        color_scalars = self.colorize("diff_holes", base=0)
        vpl.mesh_plot(self.stl_mesh, scalars=color_scalars)

        print()
        print("Processing holes")
        self.stl_mesh = self.fill_holes()
        self.stl_mesh.translate(translation=np.array([0, 0, 2 * (self.stl_mesh.max_[2] - self.stl_mesh.min_[2])]))
        self.fill_mesh_dicts()
        self.find_holes()

        # Plot the mesh with holes filled
        color_scalars = self.colorize("hole_edges", base=10)
        vpl.mesh_plot(self.stl_mesh, scalars=color_scalars)

        # Show the figure
        vpl.show()

    def print_mesh_info(self):
        print("STL is closed:", self.stl_mesh.is_closed())
        print("Mesh data length:", len(self.stl_mesh.data))
        print("Number of unique mesh points:", len(self.mesh_points_dict))
        v = len(self.mesh_points_dict)
        e = len(self.mesh_edges_dict)
        f = len(self.stl_mesh.data)
        print("V - number of mesh vertices:", v)
        print("E - number of mesh edges:", e)
        print("F - number of mesh faces (triangles):", f)
        print("Euler’s Formula check: V - E + F =", (v - e + f))

    def fill_mesh_dicts(self):
        # extract mesh points and put in the dictionary
        self.fill_points_dict()
        # extract mesh edges and put in the dictionary
        self.fill_edges_dict()
        # print mesh info
        self.print_mesh_info()

    def fill_points_dict(self):
        self.mesh_points_dict = {}
        for i in range(len(self.stl_mesh.data)):
            # points
            v = tuple(self.stl_mesh.vectors[i][0])
            if v in self.mesh_points_dict:
                self.mesh_points_dict[v].append((i, 0))
            else:
                self.mesh_points_dict[v] = [(i, 0)]
            v = tuple(self.stl_mesh.vectors[i][1])
            if v in self.mesh_points_dict:
                self.mesh_points_dict[v].append((i, 1))
            else:
                self.mesh_points_dict[v] = [(i, 1)]
            v = tuple(self.stl_mesh.vectors[i][2])
            if v in self.mesh_points_dict:
                self.mesh_points_dict[v].append((i, 2))
            else:
                self.mesh_points_dict[v] = [(i, 2)]

    def fill_edges_dict(self):
        self.mesh_edges_dict = {}
        for i in range(len(self.stl_mesh.vectors)):
            # edges
            e = (tuple(self.stl_mesh.vectors[i][0]), tuple(self.stl_mesh.vectors[i][1]))
            e_inv = (tuple(self.stl_mesh.vectors[i][1]), tuple(self.stl_mesh.vectors[i][0]))
            if e in self.mesh_edges_dict:
                self.mesh_edges_dict[e].append(i)
            elif e_inv in self.mesh_edges_dict:
                self.mesh_edges_dict[e_inv].append(i)
            else:
                self.mesh_edges_dict[e] = [i]
            e = (tuple(self.stl_mesh.vectors[i][1]), tuple(self.stl_mesh.vectors[i][2]))
            e_inv = (tuple(self.stl_mesh.vectors[i][2]), tuple(self.stl_mesh.vectors[i][1]))
            if e in self.mesh_edges_dict:
                self.mesh_edges_dict[e].append(i)
            elif e_inv in self.mesh_edges_dict:
                self.mesh_edges_dict[e_inv].append(i)
            else:
                self.mesh_edges_dict[e] = [i]
            e = (tuple(self.stl_mesh.vectors[i][0]), tuple(self.stl_mesh.vectors[i][2]))
            e_inv = (tuple(self.stl_mesh.vectors[i][2]), tuple(self.stl_mesh.vectors[i][0]))
            if e in self.mesh_edges_dict:
                self.mesh_edges_dict[e].append(i)
            elif e_inv in self.mesh_edges_dict:
                self.mesh_edges_dict[e_inv].append(i)
            else:
                self.mesh_edges_dict[e] = [i]

    def create_ref_mesh(self):
        # ref mesh
        # Read mesh from infile and output cleaned mesh to outfile
        pymeshfix.clean_from_file(self.filename, self.filename[:-4] + "_fixed.stl")
        ref_stl_mesh = mesh.Mesh.from_file(self.filename[:-4] + "_fixed.stl", calculate_normals=False)
        ref_stl_mesh.translate(translation=np.array([0, 0, -2 * (self.stl_mesh.max_[2] - self.stl_mesh.min_[2])]))

        # add the mesh to the vtk scene
        vpl.mesh_plot(ref_stl_mesh)

    def colorize(self, instance="shared_vertices", base=0, param=0) -> np.ndarray:
        """
        :type instance: string
        :type base: int
        :type param: int
        """
        color_scalars = np.ones(shape=self.stl_mesh.x.shape) * base
        if instance == "shared_vertices":
            shared_triangles: Dict[Union[int, Any], Union[int, Any]] = {}
            for point in self.mesh_points_dict:
                for position in self.mesh_points_dict[point]:
                    used_in = len(self.mesh_points_dict[point])
                    if used_in in shared_triangles:
                        shared_triangles[used_in] += 1
                    else:
                        shared_triangles[used_in] = 1
                    color_scalars[position[0]][position[1]] = used_in
            for tri_number in shared_triangles:
                shared_triangles[tri_number] = shared_triangles[tri_number] // tri_number
            print("The mesh has vertices with shared triangles:", shared_triangles)
        elif instance == "tri_with_shared_vertices":
            for point in self.mesh_points_dict:
                for position in self.mesh_points_dict[point]:
                    if len(self.mesh_points_dict[point]) == param:
                        color_scalars[position[0]] = [base + 1, base + 1, base + 1]
        elif instance == "hole_edges":
            for edge in self.hole_edges:
                color_scalars[self.hole_edges[edge]] = [base + 1, base + 1, base + 1]
        elif instance == "diff_holes":
            for i in range(len(self.holes)):
                for j in range(len(self.holes[i]) - 1):
                    edge = (self.holes[i][j], self.holes[i][j + 1])
                    if edge in self.hole_edges:
                        color_scalars[self.hole_edges[edge]] = [base + 1 + i, base + 1 + i, base + 1 + i]
                    else:
                        edge = (self.holes[i][j + 1], self.holes[i][j])
                        color_scalars[self.hole_edges[edge]] = [base + 1 + i, base + 1 + i, base + 1 + i]
        return color_scalars

    def find_holes(self):
        self.hole_edges = {}
        for edge in self.mesh_edges_dict:
            if len(self.mesh_edges_dict[edge]) == 1:
                self.hole_edges[edge] = self.mesh_edges_dict[edge][0]
        print('Holes have', len(self.hole_edges),'edges')
        holes_unique_points = set()
        for edge in self.hole_edges:
            holes_unique_points.add(edge[0])
            holes_unique_points.add(edge[1])
        self.holes_unique_points = list(holes_unique_points)
        self.holes = []
        for edge in self.hole_edges:
            self.holes.append(list(edge))
        temp_holes = []
        num_holes = len(self.holes)
        while len(self.holes):
            hole = self.holes.pop()
            temp_holes.append(hole)
            for i in range(len(self.holes)):
                if self.holes[i][0] == hole[-1]:
                    self.holes[i] = hole + self.holes[i][1:]
                    temp_holes.pop()
                    break
                elif self.holes[i][-1] == hole[0]:
                    self.holes[i] = self.holes[i] + hole[1:]
                    temp_holes.pop()
                    break
                elif self.holes[i][-1] == hole[-1]:
                    hole.pop()
                    while len(hole):
                        self.holes[i].append(hole.pop())
                    temp_holes.pop()
                    break
                elif self.holes[i][0] == hole[0]:
                    rev_hole = []
                    while len(hole):
                        rev_hole.append(hole.pop())
                    self.holes[i] = rev_hole + self.holes[i][1:]
                    temp_holes.pop()
                    break
            if len(self.holes) == 0 and num_holes != len(temp_holes):
                self.holes = temp_holes
                num_holes = len(self.holes)
                temp_holes = []
        self.holes = temp_holes
        print("Number of holes:", len(self.holes))
        holes_distribution = {}
        for hole in self.holes:
            hole_len = len(hole)
            if hole_len in holes_distribution:
                holes_distribution[hole_len] += 1
            else:
                holes_distribution[hole_len] = 1
        for stat in holes_distribution:
            print(holes_distribution[stat], "holes have", stat, "edges")

    def fill_holes(self):
        new_tris = []
        membranes = []
        while self.holes:
            hole = np.array(self.holes.pop())
            if np.shape(hole)[0] == 2:
                edge = (tuple(hole[0]),tuple(hole[1]))
                if edge in self.hole_edges:
                    membranes.append(self.hole_edges[edge])
                else:
                    edge = (edge[1],edge[0])
                    membranes.append(self.hole_edges[edge])
            else:
                center = hole.mean(0)
                tri_num = len(hole) - 1
                new_tri = np.zeros(tri_num, dtype=self.stl_mesh.dtype)
                for i in range(tri_num):
                    new_tri[i][0] = np.cross(hole[i+1] - center, hole[i] - center)
                    new_tri[i][0] = new_tri[i][0] / np.linalg.norm(new_tri[i][0])
                    new_tri[i][1] = [center, hole[i+1], hole[i]]
                new_tris.append(new_tri)
        new_data = self.stl_mesh.data
        if membranes:
            new_data = np.delete(self.stl_mesh.data, membranes, 0)
        if new_tris:
            tris = new_tris.pop()
            for new_tri in new_tris:
                tris = np.append(tris, new_tri, axis=0)
            tri_mesh: Mesh = mesh.Mesh(tris.copy())
            tri_mesh.translate(translation=np.array([0, 0, 4 * (self.stl_mesh.max_[2] - self.stl_mesh.min_[2])]))
            # put added triangles in the vtk scene
            vpl.mesh_plot(tri_mesh)
            return mesh.Mesh(np.append(new_data, tris,axis=0))
        else:
            return mesh.Mesh(self.stl_mesh.data)
