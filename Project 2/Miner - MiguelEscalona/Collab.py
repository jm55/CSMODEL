import numpy as np
import pandas as pd

class CollaborativeFiltering(object):

    def __init__(self, k):
        """Class constructor for KMeans
        Arguments:
            k {int} -- number of similar items to consider
        """
        self.k = k

    def get_row_mean(self, data):
        """Returns the mean of each row in the DataFrame or the mean of the
        Series. If the parameter data is a DataFrame, the function will
        return a Series containing the mean of each row in the DataFrame. If
        the parameter data is a Series, the function will return a np.float64
        which is the mean of the Series. This function should not consider
        blank ratings represented as NaN.

        Arguments:
            data {DataFrame or Series} -- dataset
        Returns:
            Series or np.float64 -- row mean
        """
        if isinstance(data, pd.DataFrame):
            return data.mean(axis=1)
        elif isinstance(data, pd.Series):
            return data.mean()

    def normalize_data(self, data, row_mean):
        """Returns the data normalized by subtracting the row mean.

        For the arguments point1 and point2, you can only pass these
        combinations of data types:
        - DataFrame and Series -- returns DataFrame
        - Series and np.float64 -- returns Series

        For a DataFrame and a Series, if the shape of the DataFrame is
        (3, 2), the shape of the Series should be (3,) to enable broadcasting.
        This operation will result to a DataFrame of shape (3, 2)

        Arguments:
            data {DataFrame or Series} -- dataset
            row_mean {Series or np.float64} -- mean of each row
        Returns:
            DataFrame or Series -- normalized data
        """
        if isinstance(data, pd.DataFrame) and isinstance(row_mean, pd.Series):
            return data.subtract(row_mean, axis=0)
        elif isinstance(data, pd.Series) and isinstance(row_mean, float):
            return data.subtract(row_mean)

        # Normalize the parameter data by parameter row_mean.
        # HINT: Use pandas.DataFrame.subtract() or pandas.Series.subtract()
        # functions.
        pass

    def get_cosine_similarity(self, vector1, vector2):
        """Returns the cosine similarity between two vectors. These vectors can
        be represented as 2 Series objects. This function can also compute the
        cosine similarity between a list of vectors (represented as a
        DataFrame) and a single vector (represented as a Series), using
        broadcasting.

        For the arguments vector1 and vector2, you can only pass these
        combinations of data types:
        - Series and Series -- returns np.float64
        - DataFrame and Series -- returns pd.Series

        For a DataFrame and a Series, if the shape of the DataFrame is
        (3, 2), the shape of the Series should be (2,) to enable broadcasting.
        This operation will result to a Series of shape (3,)

        Arguments:
            vector1 {Series or DataFrame} - vector
            vector2 {Series or DataFrame} - vector
        Returns:
            np.float64 or pd.Series -- contains the cosine similarity between
            two vectors
        """
        rt = None
        if isinstance(vector1, pd.Series) and isinstance(vector2, pd.Series):
            pow2_v1 = np.power(vector1,2)
            pow2_v2 = np.power(vector2,2)
            numerator = (vector1*vector2).sum()
            denominator = np.sqrt(pow2_v1.sum()) * np.sqrt(pow2_v2.sum())
            return numerator/denominator
        elif isinstance(vector1, pd.DataFrame) and isinstance(vector2, pd.Series):
            l = []
            for i in range(vector1.shape[0]):
                l.append(self.get_cosine_similarity(vector1.iloc[i],vector2))
            l = pd.Series(l)
            l.index = vector1.index.to_list()
            return l
        # TODO: Compute the cosine similarity between the two parameters.
        # HINT: Use np.sqrt() and pandas.DataFrame.sum() and/or
        # pandas.Series.sum() functions.

        pass

    def get_k_similar(self, data, vector):
        """Returns two values - the indices of the top k similar items to the
        vector from the dataset, and a Series representing their similarity
        values to the vector. We find the top k items from the data which
        are highly similar to the vector.

        Arguments:
            data {DataFrame} -- dataset
            vector {Series} -- vector
        Returns:
            Index -- indices of the top k similar items to the vector
            Series -- computed similarity of the top k similar items to the
            vector
        """
        norm_data = self.normalize_data(data,self.get_row_mean(data))
        norm_vector = self.normalize_data(vector,self.get_row_mean(vector))
        sim = self.get_cosine_similarity(norm_data,norm_vector)
        return sim.nlargest(self.k).index.to_list(), sim

    def get_rating(self, data, index, column):
        """Returns the extrapolated rating for the item in row index from the
        user in column column based on similar items.

        The algorithm for this function is as follows:
        1. Get k similar items.
        2. Compute for the rating using the similarity values and the raw
        ratings for the k similar items.

        Arguments:
            data {DataFrame} -- dataset
            index {int} -- row of the item
            column {int} -- column of the user
        Returns:
            np.float64 -- extrapolated rating based on similar ratings
        """
        # TODO: Complete this function.
        before_df = data.iloc[:index, :]
        after_df = data.iloc[index + 1:, :]
        new_data = pd.concat([before_df, after_df])
        vector = data.iloc[index, :]

        # TODO: Get top k items that are similar to the parameter vector
        # HINT: Use the get_k_similar() function that we have defined in this
        # class
        sim = self.get_k_similar(new_data,vector)
        # TODO: Compute for the rating using the similarity values and the raw
        # ratings for the k similar items.
        numerator = None
        idx = sim[0]
        #col will dictate user while idx[i] will dictate similarities
        rating = (sim[1]*new_data.iloc[:,column]).sum() / sim[1].sum()
        return rating
