<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">

<h3 align="center">Hole fixer</h3>

  <p align="center">
    It is a demonstration program for holes fixing algorithm
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Person STL Processing](https://github.com/Dimdimovich/HoleFixer/blob/main/HoleFixer.png?raw=true)

Here's a project for a demonstration of the hole-fixing algorithm. 
The class `STLProcessor` from `tools/stlProcessor.py` implements the main components of the algorithm. It uses the `find_holes` method to find cracks in the geometry. This method exploits an additional data structure, `mesh_edges_dict`. It is a dictionary with edges as keys and faces indices as values. The algorithm constructs holes described as edges set belonging to only one face. Each hole in the generated list is a consequent list of vertices from previously selected edges.

`fill_holes` is the second method of the `STLProcessor` class that implements the hole processing algorithm. It fills holes with patches. These patches are made of triangles starting at hole centroids and relying on hole edges. Moreover, this procedure cleans the mesh from a specified form of hanging triangles. It removes lonely triangles with only one free edge.

The program shows the result as four meshes. The first one is the grey mesh generated with `pymeshfix` as a reference mesh. The second one is the original mesh with holes and hanging triangles hihglighted. The third one is the repaired mesh with unfixed issues highlighted. The last one is the grey mesh of added triangles. 

The proposed algorithm has several weaknesses:

1. It does not analyze the form of holes and their positions. Therefore, the centroid strategy of patching can lead to self-intersection of the processed mesh. Moreover, in some cases, more natural hole fixing supposes the merging of two pieces of 2D surfaces. 

2. It does not clean the mesh from other hanging face types.

3. It does not prevent the mesh from self-intersections.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![NumPy][NumPy]][NumPy-url]
* [![VTK][VTK]][VTK-url]
* [![PyVista][PyVista]][PyVista-url]
* [![PyQt][PyQt]][PyQt-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

### Prerequisites

The project was created with python version 3.6.3

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Dimdimovich/HoleFixer.git
   ```
2. activate
  
  on Windows
   ```sh
   ./venv/Scripts/Activate
   ```
  on OSX/Linux
   ```sh
   ./venv/bin/activate
   ```
3. Install used packages
   ```sh
   python -m pip install pyqt6
   ```
   ```sh
   python -m pip install numpy-stl
   ```
   ```sh
   python -m pip install vtkplotlib==1.5.1 --force-reinstall
   ```
   ```sh
   python -m pip install pymeshfix
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Run the script with 

```sh
python main.py
```

Click the STL button and choose an stl file you want to process. See the result of holes fixing in the new window. Summary of the processing is avaliable in the console.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Dmitry Popov - dimdimovich@icloud.com

Project Link: [https://github.com/Dimdimovich/HoleFixer](https://github.com/Dimdimovich/HoleFixer)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/Dimdimovich/HoleFixer/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/ddpopov
[product-screenshot]: images/screenshot.png
[NumPy]: https://img.shields.io/badge/numpy-000000?style=for-the-badge&logo=numpy&logoColor=white
[NumPy-url]: https://numpy.org/
[VTK]: https://img.shields.io/badge/vtk-000000?style=for-the-badge&logo=vtk&logoColor=white
[VTK-url]: https://vtkplotlib.readthedocs.io/
[PyVista]: https://img.shields.io/badge/pyvista-000000?style=for-the-badge&logo=pyvista&logoColor=white
[PyVista-url]: https://pymeshfix.pyvista.org/
[PyQt]: https://img.shields.io/badge/pyqt-000000?style=for-the-badge&logo=qt&logoColor=white
[PyQt-url]: https://www.riverbankcomputing.com/software/pyqt/
[product-screenshot]: https://github.com/Dimdimovich/HoleFixer/blob/main/HoleFixer.png?raw=true
