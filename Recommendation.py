import numpy as np
from sklearn.metrics.pairwise import cosine_similarity


def cosine_similarity_matrix(user_item_matrix):
    similarity = cosine_similarity(user_item_matrix)
    np.fill_diagonal(similarity, 0)
    return similarity


def get_top_k_neighbours(similarity_matrix, user_id, k):
    user_similarity = similarity_matrix[user_id]
    neighbors = np.argsort(-user_similarity)
    return neighbors[:k]
    

def recomend_items(user_id,item_id,user_item_matrix,similarity_matrix,k):
    top_k_neighbors = get_top_k_neighbours(similarity_matrix, user_id, k)
    neighbour_rating = user_item_matrix[top_k_neighbors,item_id]
    similarity_scores = similarity_matrix[user_id, top_k_neighbors]

    valid_ratings_mask = neighbour_rating > 0
    valid_ratings = neighbour_rating[valid_ratings_mask]
    valid_similarities = similarity_scores[valid_ratings_mask]


    if len(valid_ratings)>1:
        predicted = np.dot(valid_similarities,valid_similarities)/np.sum(valid_similarities)
    elif len(valid_ratings)==1:
        predicted = (valid_similarities[0]*valid_ratings[0])/valid_similarities[0]
    else:
        predicted = 0

    return predicted

    

user_item_matrix = np.array([
    [4, 0, 3, 5, 2, 0, 0, 4],
    [5, 3, 0, 4, 0, 4, 2, 1],
    [3, 5, 4, 0, 4, 0, 3, 0],
    [0, 4, 0, 5, 0, 3, 0, 5],
    [4, 0, 3, 4, 5, 0, 2, 0],
    [3, 4, 0, 0, 4, 5, 0, 0],
    [0, 2, 4, 5, 0, 0, 5, 4],
    [5, 0, 0, 0, 3, 4, 4, 2],
    [4, 4, 3, 0, 2, 0, 5, 3],
    [0, 5, 4, 3, 0, 4, 2, 5]
])



similarity_matrix = cosine_similarity_matrix(user_item_matrix)
print(similarity_matrix)

user_id = 3
item_id = 1
k = 2

rating = recomend_items(user_id,item_id,user_item_matrix,similarity_matrix,k)
print(rating)