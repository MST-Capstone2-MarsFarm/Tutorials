#Import external modules
import numpy as np
import math

#used to calculate roi points and radius automatically.

def auto_roi(labeled_objects_array: np.ndarray=None) -> list[list[tuple[int, int]], int]:
    labeled_objects_array = labeled_objects_array
    #the number of unique plants should all the unique np values from the array that aren't zero
    #since 0 is counted as a number, should be len - 1
    num_plants = len(np.unique(labeled_objects_array)) - 1
    center_points = [] 
    
   #calculate the euclidean distance between two points

    #the 'main' function of the class
    def get_roi_centers_and_individual_images():        
        def _euclidian_distance(point1: tuple, point2: tuple):
            """Calculate the Euclidean distance between two points."""
            return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    
        #get minimum of either distance to edge or distance to another plant
        def _min_no_intersect_euclidean_distance():
            #get minimum distance of any of the points to an edge
            def _min_distance_to_edge():
                # x is 0th index, y is 1th index in tuple (x, y)
                height, width = np.shape(labeled_objects_array)[:2]
                x_vals = [x for x, y in center_points]
                y_vals = [y for x, y in center_points]
                xmin, xmax = min(x_vals), max(x_vals)
                ymin, ymax = min(y_vals), max(y_vals)
                distances_to_edge = [xmin, width-xmax, ymin, height-ymax]
                return min(distances_to_edge)
            
            """Find the maximum Euclidean distance between any two points in the list."""
            if len(center_points) <= 1: return 0
            n = len(center_points)
        
            min_distance = _min_distance_to_edge()
        
            #calculate euclidean distances between points and to the edge of the graph
            for i in range(1, n):
                for j in range(i + 1, n):
                    distance = _euclidian_distance(center_points[i], center_points[j])
                    min_distance = min(min_distance, distance)
            return math.floor(min_distance)

        #no lower bound for the radius
        #this should help accomadate identifying small individual sprouts
        max_circle_radius_size = 0
        
        for number in range(1, num_plants+1):
            # Create a mask for the current number
            mask = labeled_objects_array == number
            
            # Find indices where the mask is True
            cols, rows = np.nonzero(mask)
            
            if rows.size > 0 and cols.size > 0:
                # Calculate bounds
                #rows = y axis, columns = x axis, depth = z axis
                min_row, max_row = np.min(rows), np.max(rows)
                min_col, max_col = np.min(cols), np.max(cols)
    
                middle_row = (min_row + max_row) // 2
                middle_col = (min_col + max_col) // 2

                #calculate the radius of a circle that would fit the entire plant
                #radius = diameter / 2
                point1 = (min_row, min_col)
                point2 = (max_row, max_col)
                encapsulating_circle_radius = _euclidian_distance(point1, point2) // 2

                #once that's done, then iteratively calculate the max radius size for
                max_circle_radius_size = max(max_circle_radius_size, encapsulating_circle_radius)
    
                #calculate the radius 
    
                center_points.append((middle_row, middle_col))                                                                        
                
            else:
                print(f"no indices for {number}")
                continue
        #calculate minimum distance either to edge, distance to another plant, or (the largest radius or any other plant with a floor of 50)
        optimal_radius_size = min(_min_no_intersect_euclidean_distance(), encapsulating_circle_radius)
        
        return center_points, optimal_radius_size
    
    return get_roi_centers_and_individual_images()