import sys, os
import numpy as np
import math

#used to calculate roi points and radius automatically.
class auto_roi:
    def __init__(self, img: np.ndarray=None, labeled_objects_array: np.ndarray=None):
        self.img = img
        self.labeled_objects_array = labeled_objects_array
        #the number of unique plants should all the unique np values from the array that aren't zero
        #since 0 is counted as a number, should be len - 1
        self.num_plants = len(np.unique(self.labeled_objects_array)) - 1
        self.center_points = []

    #calculate the euclidean distance between two points
    def _euclidian_distance(self, point1: tuple, point2: tuple):
        """Calculate the Euclidean distance between two points."""
        return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

    #get minimum distance of any of the points to an edge
    def _min_distance_to_edge(self):
        # x is 0th index, y is 1th index in tuple (x, y)
        height, width = np.shape(self.img)[:2]
        x_vals = [x for x, y in self.center_points]
        y_vals = [y for x, y in self.center_points]
        xmin, xmax = min(x_vals), max(x_vals)
        ymin, ymax = min(y_vals), max(y_vals)
        distances_to_edge = [xmin, width-xmax, ymin, height-ymax]
        return min(distances_to_edge)
    
    #get minimum of either distance to edge or distance to another plant
    def _min_no_intersect_euclidean_distance(self):
        """Find the maximum Euclidean distance between any two points in the list."""
        if len(self.center_points) <= 1: return 0
        n = len(self.center_points)
    
        min_distance = self._min_distance_to_edge()
    
        #calculate euclidean distances between points and to the edge of the graph
        for i in range(1, n):
            for j in range(i + 1, n):
                distance = self._euclidian_distance(self.center_points[i], self.center_points[j])
                min_distance = min(min_distance, distance)
        return math.floor(min_distance)

    #the 'main' function of the class
    def get_roi_centers_and_individual_images(self):

        #no lower bound for the radius
        #this should help accomadate identifying small individual sprouts
        max_circle_radius_size = 0
        
        for number in range(1, self.num_plants+1):
            # Create a mask for the current number
            mask = self.labeled_objects_array == number
            
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
                encapsulating_circle_radius = self._euclidian_distance((min_row, min_col), (max_row, max_col)) // 2

                #once that's done, then iteratively calculate the max radius size for
                max_circle_radius_size = max(max_circle_radius_size, encapsulating_circle_radius)
    
                #calculate the radius 
    
                self.center_points.append((middle_row, middle_col))
    
                '''
                #get rgb images clipped to bounds of labels, export to image file
                chopped_image_rgb = img0[min_col:max_col+1, min_row:max_row+1, :]
                output_path_rgb = os.path.join(args.rgb_outdir, f"plant_rgb_{number}.png")
                pcv.print_image(chopped_image_rgb, output_path_rgb)
    
                #get black and white image bounds,  export to image file
                chopped_image_bw = labeled_mask[min_col:max_col+1, min_row:max_row+1]
                chopped_image_bw = chopped_image_bw.astype(bool).astype('uint8') * 255
                p = Image.fromarray(chopped_image_bw)
                output_path_bw = os.path.join(args.bw_outdir, f"plant_bw_{number}.png")
                p.save(output_path_bw)'''
                                                                        
                
            else:
                print(f"no indices for {number}")
                continue
        #calculate minimum distance either to edge, distance to another plant, or (the largest radius or any other plant with a floor of 50)
        optimal_radius_size = min(self._min_no_intersect_euclidean_distance(), encapsulating_circle_radius)
        
        return self.center_points, optimal_radius_size