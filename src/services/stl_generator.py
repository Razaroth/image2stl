"""STL file generation from height maps."""

import numpy as np
import trimesh
from trimesh.creation import box
from scipy import ndimage


class STLGenerator:
    """Generate STL files from height maps."""

    @staticmethod
    def create_mesh_from_height_map(
        X: np.ndarray, Y: np.ndarray, Z: np.ndarray
    ) -> trimesh.Trimesh:
        """
        Create a 3D mesh from height map data with closed bottom.

        Args:
            X: X coordinates (mesh grid)
            Y: Y coordinates (mesh grid)
            Z: Z heights (mesh grid)

        Returns:
            Trimesh object representing the 3D model
        """
        height, width = X.shape
        
        # Find minimum Z value for the base
        min_z = np.min(Z)
        
        # Create vertices: top surface vertices + bottom surface vertices
        top_vertices = np.column_stack([X.flat, Y.flat, Z.flat])
        bottom_vertices = np.column_stack([X.flat, Y.flat, np.full_like(Z.flat, min_z)])
        
        # Combine all vertices
        vertices = np.vstack([top_vertices, bottom_vertices])
        
        # Create faces
        faces = []
        num_top_verts = height * width
        
        # Top surface faces
        for i in range(height - 1):
            for j in range(width - 1):
                # Vertex indices for this quad on top
                v0 = i * width + j
                v1 = i * width + (j + 1)
                v2 = (i + 1) * width + (j + 1)
                v3 = (i + 1) * width + j
                
                # Create two triangles from quad (top surface)
                faces.append([v0, v1, v2])
                faces.append([v0, v2, v3])
        
        # Bottom surface faces (reverse winding for correct normals)
        for i in range(height - 1):
            for j in range(width - 1):
                # Vertex indices for this quad on bottom
                v0 = num_top_verts + i * width + j
                v1 = num_top_verts + i * width + (j + 1)
                v2 = num_top_verts + (i + 1) * width + (j + 1)
                v3 = num_top_verts + (i + 1) * width + j
                
                # Create two triangles from quad (bottom surface, reverse winding)
                faces.append([v0, v2, v1])
                faces.append([v0, v3, v2])
        
        # Side walls - connect top and bottom edges
        # Top edge (i=0)
        for j in range(width - 1):
            v_top_0 = 0 * width + j
            v_top_1 = 0 * width + (j + 1)
            v_bot_0 = num_top_verts + 0 * width + j
            v_bot_1 = num_top_verts + 0 * width + (j + 1)
            
            faces.append([v_top_0, v_bot_0, v_bot_1])
            faces.append([v_top_0, v_bot_1, v_top_1])
        
        # Bottom edge (i=height-1)
        for j in range(width - 1):
            v_top_0 = (height - 1) * width + j
            v_top_1 = (height - 1) * width + (j + 1)
            v_bot_0 = num_top_verts + (height - 1) * width + j
            v_bot_1 = num_top_verts + (height - 1) * width + (j + 1)
            
            faces.append([v_top_0, v_bot_1, v_bot_0])
            faces.append([v_top_0, v_top_1, v_bot_1])
        
        # Left edge (j=0)
        for i in range(height - 1):
            v_top_0 = i * width + 0
            v_top_1 = (i + 1) * width + 0
            v_bot_0 = num_top_verts + i * width + 0
            v_bot_1 = num_top_verts + (i + 1) * width + 0
            
            faces.append([v_top_0, v_bot_1, v_bot_0])
            faces.append([v_top_0, v_top_1, v_bot_1])
        
        # Right edge (j=width-1)
        for i in range(height - 1):
            v_top_0 = i * width + (width - 1)
            v_top_1 = (i + 1) * width + (width - 1)
            v_bot_0 = num_top_verts + i * width + (width - 1)
            v_bot_1 = num_top_verts + (i + 1) * width + (width - 1)
            
            faces.append([v_top_0, v_bot_0, v_bot_1])
            faces.append([v_top_0, v_bot_1, v_top_1])
        
        faces = np.array(faces, dtype=np.int64)
        
        # Create mesh
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
        
        return mesh

    @staticmethod
    def add_base_to_mesh(mesh: trimesh.Trimesh, base_height: float = 2.0) -> trimesh.Trimesh:
        """
        Add a solid base to the mesh.

        Args:
            mesh: Input mesh
            base_height: Height of the base

        Returns:
            Mesh with base attached
        """
        # Get mesh bounds
        bounds = mesh.bounds
        min_x, min_y, _ = bounds[0]
        max_x, max_y, _ = bounds[1]
        
        # Create base box
        center_x = (min_x + max_x) / 2
        center_y = (min_y + max_y) / 2
        base_z = -base_height / 2
        
        width = max_x - min_x
        depth = max_y - min_y
        
        base = box(
            extents=[width, depth, base_height],
            transform=trimesh.transformations.translation_matrix(
                [center_x, center_y, base_z]
            ),
        )
        
        # Combine meshes
        combined = trimesh.util.concatenate([mesh, base])
        
        return combined

    @staticmethod
    def save_stl(mesh: trimesh.Trimesh, output_path: str) -> None:
        """
        Save mesh to STL file.

        Args:
            mesh: Trimesh object
            output_path: Path to save the STL file
        """
        mesh.export(output_path)

    @staticmethod
    def make_watertight(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """
        Make mesh watertight by filling holes and removing non-manifold geometry.

        Args:
            mesh: Input mesh

        Returns:
            Watertight mesh
        """
        try:
            # Remove degenerate faces if method exists
            if hasattr(mesh, 'remove_degenerate_faces'):
                mesh.remove_degenerate_faces()
        except Exception:
            pass
        
        try:
            # Remove duplicate faces if method exists
            if hasattr(mesh, 'remove_duplicate_faces'):
                mesh.remove_duplicate_faces()
        except Exception:
            pass
        
        try:
            # Merge vertices to clean up geometry
            if hasattr(mesh, 'merge_vertices'):
                mesh.merge_vertices()
        except Exception:
            pass
        
        try:
            # Fill holes
            if hasattr(mesh, 'fill_holes'):
                mesh.fill_holes()
        except Exception:
            pass
        
        try:
            # Fix normals to ensure proper orientation
            if hasattr(mesh, 'fix_normals'):
                mesh.fix_normals()
        except Exception:
            pass
        
        return mesh

    @staticmethod
    def close_mesh_bottom(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
        """
        Close the bottom of the mesh with a base plate.

        Args:
            mesh: Input mesh

        Returns:
            Mesh with closed bottom
        """
        bounds = mesh.bounds
        min_z = bounds[0, 2]
        
        # Get the vertices at the bottom
        bottom_verts = mesh.vertices[mesh.vertices[:, 2] <= min_z + 0.1]
        
        if len(bottom_verts) > 0:
            # Create a base plate
            unique_verts = np.unique(bottom_verts.astype(np.int32))
            if len(unique_verts) > 0:
                mesh.fix_normals()
        
        return mesh

    @staticmethod
    def get_mesh_info(mesh: trimesh.Trimesh) -> dict:
        """
        Get information about the mesh.

        Args:
            mesh: Trimesh object

        Returns:
            Dictionary with mesh statistics
        """
        return {
            "vertices": len(mesh.vertices),
            "faces": len(mesh.faces),
            "bounds": mesh.bounds.tolist(),
            "volume": float(mesh.volume),
            "is_watertight": mesh.is_watertight,
        }
