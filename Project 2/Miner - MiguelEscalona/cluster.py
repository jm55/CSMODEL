import numpy as np
import pandas as pd

class KMeans(object):

    def __init__(self, k, start_var, end_var, num_observations, data):
        """Class constructor for KMeans
        Arguments:
            k {int} -- number of clusters to create from the data
            start_var {int} -- starting index of the variables (columns) to
            consider in creating clusters from the dataset. This is
            useful for excluding some columns for clustering.
            end_var {int} -- ending index of the variables (columns) to
            consider in creating clusters from the dataset. This is
            useful for excluding some columns for clustering.
            num_observations {int} -- total number of observations (rows) in
            the dataset.
            data {DataFrame} -- the dataset to cluster
        """
        np.random.seed(1)
        self.k = k
        self.start_var = start_var
        self.end_var = end_var
        self.num_observations = num_observations
        self.columns = [i for i in data.columns[start_var:end_var]]
        self.centroids = pd.DataFrame(columns=self.columns)

    def initialize_centroids(self, data):
        """Returns initial centroids. This function picks a random point from
        the dataset as the first centroid, then iteratively picks points that
        are farthest from the current set of centroids.

        The algorithm for this initialization is as follows:
        1. Randomly select the first centroid from the data points in the
        dataset. OK
        2. For each data point, compute its distance from each centroid in the
        current set of centroids. For each distance computed from each
        centroid, retain only the shortest distance for each data point. In
        other words, we are computing the distance of each data point from
        the nearest centroid.
        3. Select the data point with the maximum distance from the nearest
        centroid as the next centroid.
        4. Repeat steps 2 and 3 until we have k number of centroids.

        Arguments:
            data {DataFrame} -- dataset to cluster
        Returns:
            DataFrame -- contains the values of the initial location of the
            centroids.
        """
        # TODO: Complete this function.
        # Step 1: Randomly select a data point from the dataset as the first
        # centroid.
        index = np.random.randint(low=0, high=self.num_observations)
        point = data.iloc[index, self.start_var:self.end_var]
        self.centroids = self.centroids.append(point, ignore_index=True)
        sliced_data = data.iloc[:, self.start_var:self.end_var]
        #めっちゃ大変ですよ
        # Step 2: Select the remaining centroids.
        for i in range(1, self.k):
            # The variable distance is a DataFrame that will store the
            # distances of each data point from each centroid. Each column
            # represents the distance of the data point from a specific
            # centroid. Example, the value in row 3 column 0 of the DataFrame
            # distances represents the distance of data point 3 from
            # centroid 0.
            distances = pd.DataFrame()
            l=[]
            for j in range(len(self.centroids)): #for every centroid
                d = self.get_euclidean_distance(sliced_data, self.centroids.iloc[j]) #calculate euclidean
                l.append(d.to_list()) #get distance on available data
            distances = pd.DataFrame(l).transpose()
            # Hint: Use pandas.DataFrame.min() and pandas.Series.idxmax()
            min = distances.min(axis=1) #Get the minimum distance of each data point from centroid.
            index = min.idxmax()# get the index of the data point with the maximum distance from the nearest centroid and store it to variable index.
            point = data.iloc[index, self.start_var:self.end_var]
            self.centroids = self.centroids.append(point, ignore_index=True)
            #print(self.centroids)
        return self.centroids

    def get_euclidean_distance(self, point1, point2):
        """Returns the Euclidean distance between two data points. These
        data points can be represented as 2 Series objects. This function can
        also compute the Euclidean distance between a list of data points
        (represented as a DataFrame) and a single data point (represented as
        a Series), using broadcasting.

        The Euclidean distance can be computed by getting the square root of
        the sum of the squared difference between each variable of each data
        point.

        For the arguments point1 and point2, you can only pass these
        combinations of data types:
        - Series and Series -- returns np.float64
        - DataFrame and Series -- returns pd.Series

        For a DataFrame and a Series, if the shape of the DataFrame is
        (3, 2), the shape of the Series should be (2,) to enable broadcasting.
        This operation will result to a Series of shape (3,)

        Arguments:
            point1 {Series or DataFrame} - data point
            point2 {Series or DataFrame} - data point
        Returns:
            np.float64 or pd.Series -- contains the Euclidean distance
            between the data points.
        """
        # TODO: Implement this function based on the documentation.
        if isinstance(point1, pd.Series)and isinstance(point2, pd.Series):
            #both series; returns as float
            return np.sqrt(np.power(point1[0]-point2[0],2)+np.power(point1[1]-point2[1],2))
        elif isinstance(point1, pd.DataFrame) and isinstance(point2, pd.Series):
            list = []
            for i in range(point1.shape[0]):
                list.append(self.get_euclidean_distance(point1.iloc[i],point2.tail(4)))
            s = pd.Series(list)
            #s = s[s!=0]
            return s
        # Hint: Use the pandas.Series.sum() and the numpy.sqrt() functions.

    def group_observations(self, data):
        """Returns the clusters of each data point in the dataset given
        the current set of centroids. Suppose this function is given 100 data
        points to cluster into 3 groups, the function returns a Series of
        shape (100,), where each value is between 0 to 2.

        Arguments:
            data {DataFrame} -- dataset to cluster
        Returns:
            Series -- represents the cluster of each data point in the dataset.
        """
        # TODO: Complete this function.

        # The variable distance is a DataFrame that will store the distances
        # of each data point from each centroid. Each column represents the
        # distance of the data point from a specific centroid. Example, the
        # value in row 3 column 0 of the DataFrame distances represents the
        # distance of data point 3 from centroid 0.
        distance = pd.DataFrame()
        sliced_data = data.iloc[:, self.start_var:self.end_var]
        for i in range(self.k):
            distance[i] = self.get_euclidean_distance(sliced_data,self.centroids.iloc[i])
            # TODO: Get the Euclidean distance of the data from each centroid
            # then store it to a column in the DataFrame distances
            # Hint: Use the get_euclidean_distance() function that we have
            # defined in this class.
        # TODO: get the index of the lowest distance for each data point and
        # assign it to a Series named groups
        # Hint: Use pandas.DataFrame.idxmin()
        groups = distance.idxmin(axis=1)
        return groups.astype('int32')

    def adjust_centroids(self, data, groups):
        """Returns the new values for each centroid. This function adjusts
        the location of centroids based on the average of the values of the
        data points in their corresponding clusters.

        Arguments:
            data {DataFrame} -- dataset to cluster
            groups {Series} -- represents the cluster of each data point in the
            dataset.
        Returns:
            DataFrame -- contains the values of the adjusted location of the
            centroids.
        """
        # TODO: Complete this function.
        grouped_data = pd.concat([data, groups.rename('group')], axis=1)
        # TODO: Group the data points together using the group column, then
        # get their mean and store to variable centroids.
        # Hint: use pandas.DataFrame.groupby and
        # pandas.core.groupby.GroupBy.mean functions.
        centroids = grouped_data.groupby('group').mean()
        return centroids

    def train(self, data, iters):
        """Returns a Series which represents the final clusters of each data
        point in the dataset. This function stops clustering if one of the
        following is met:
        - The values of the centroids do not change.
        - The clusters of each data point do not change.
        - The maximum number of iterations is met.

        Arguments:
            data {DataFrame} -- dataset to cluster
            iters {int} -- maximum number of iterations before the clustering
            stops
        Returns:
            Series -- represents the final clusters of each data point in the
            dataset.
        """
        # TODO: Complete this function.
        cur_groups = pd.Series(-1, index=[i for i in range(self.num_observations)])
        i = 0
        flag_groups = False
        flag_centroids = False
        # While no stopping criterion has been met, do the following
        while i < iters and not flag_groups and not flag_centroids:
            # Hint: Use the group_observation() function that we have defined
            # in this class.
            groups = self.group_observations(data) #Get the clusters of the data points in the dataset and store it in variable groups.
            # Hint: Use the adjust_centroids() function that we have defined in this class.
            centroids = self.adjust_centroids(data,groups) # Adjust the centroids based on the current clusters and store it in variable centroids.
            # TODO: Check if there are changes with the clustering of the
            # data points.
            # TODO: Check if there are changes with the values of the centroids
            if not groups.equals(cur_groups):
                cur_groups = groups
            if not centroids.equals(self.centroids):
                self.centroids = centroids
            i += 1
            print('Iteration', i)

        print('Done clustering!')
        return cur_groups
