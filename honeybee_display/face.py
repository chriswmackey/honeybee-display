"""Method to translate a Face to a VisualizationSet."""
from ladybug_display.geometry3d import DisplayFace3D
from ladybug_display.visualization import VisualizationSet, ContextGeometry


def face_to_vis_set(face, color_by='type'):
    """Translate a Honeybee Face to a VisualizationSet.

    Args:
        model: A Honeybee Face object to be converted to a VisualizationSet.
        color_by: Text for the property that dictates the colors of the Face
            geometry. (Default: type). Choose from the following:

            * type
            * boundary_condition

    Returns:
        A VisualizationSet object that represents the Face with a single ContextGeometry.
    """
    # get the basic properties for geometry conversion
    color_by_attr = 'type_color' if color_by.lower() == 'type' else 'bc_color'
    # convert all geometry into DisplayFace3D
    dis_geos = _face_display_geometry(face, color_by_attr)
    # build the VisualizationSet and ContextGeometry
    con_geo = ContextGeometry(face.identifier, dis_geos)
    con_geo.display_name = face.display_name
    vis_set = VisualizationSet(face.identifier, [con_geo])
    vis_set.display_name = face.display_name
    return vis_set


def _face_display_geometry(face, color_by_attr, d_mod='SurfaceWithEdges'):
    """Get DisplayFace3D that represent a Honeybee Face."""
    dis_geos = []
    f_col = getattr(face, color_by_attr)
    dis_geos.append(DisplayFace3D(face.punched_geometry, f_col, d_mod))
    _add_display_shade(face, dis_geos, color_by_attr, d_mod)
    for ap in face._apertures:
        a_col = getattr(ap, color_by_attr)
        dis_geos.append(DisplayFace3D(ap.geometry, a_col, d_mod))
        _add_display_shade(ap, dis_geos, color_by_attr, d_mod)
    for dr in face._doors:
        d_col = getattr(dr, color_by_attr)
        dis_geos.append(DisplayFace3D(dr.geometry, d_col, d_mod))
        _add_display_shade(dr, dis_geos, color_by_attr, d_mod)
    return dis_geos


def _add_display_shade(shaded_obj, dis_geos, color_by_attr, d_mod='SurfaceWithEdges'):
    """Add display objects to represent shaded assigned to an object."""
    for shd in shaded_obj.shades:
        s_col = getattr(shd, color_by_attr)
        dis_geos.append(DisplayFace3D(shd.geometry, s_col, d_mod))
