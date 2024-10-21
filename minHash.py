import numpy as np

def create_shingles(document, k=2):
  words = document.replace('.', "").split(" ")
  shingles = set()
  for i in range(len(words)-k+1):
    shingles.add(" ".join(words[i:i+k]))
  return shingles

def shingles_matrix(shingles, documents):
  matrix = np.zeros((len(shingles), len(documents)), dtype = np.int8)
  for i, j in enumerate(shingles):
    for k in range(len(documents)):
      matrix[i][k] = j in documents[k]
  return matrix

def hash_1(x, n):
  return (x+1)%n

def hash_2(x, n):
  return (3*x+1)%n

def minhash(matrix, hashes):
  n = len(matrix[0])
  sig_mat = np.full((len(hashes), n), np.inf)
  for i in range(len(matrix)):
    for j in range(len(matrix[0])):
      if matrix[i][j] == 1:
          sig_mat[0][j] = min(sig_mat[0][j], hashes[0][i])
          sig_mat[1][j] = min(sig_mat[1][j], hashes[1][i])
    print(f"Iteration {i} : {sig_mat}")
  print()
  return sig_mat

def compare_signatures(signature_1, signature_2, threshold = 0.75):
  similarity = np.sum(signature_1 == signature_2) / len(signature_1)
  return similarity


doc1 = 'data disk search algorithm'
doc2 = 'disk search data algorithm heuristic'
doc3 = 'data disk search algorithm heuristic apple'
doc4 = 'disk data search algorithm heuristic apple'
doc5 = 'data disk search algorithm'

documents = [doc1, doc2, doc3, doc4, doc5]


shingles_1 = create_shingles(documents[0])
shingles_2 = create_shingles(documents[1])
shingles_3 = create_shingles(documents[2])
shingles_4 = create_shingles(documents[3])
shingles_5 = create_shingles(documents[4])


shingles = shingles_1.union(shingles_2).union(shingles_3).union(shingles_4).union(shingles_5)
shingles = sorted(list(shingles))
print(shingles)

hash1 = [hash_1(x, len(shingles)) for x in list(range(0, len(shingles)))]
hash2 = [hash_2(x, len(shingles)) for x in list(range(0, len(shingles)))]


matrix = shingles_matrix(shingles, documents)
print(matrix)
print()

hashes = [hash1, hash2]

sig_mat = minhash(matrix, hashes)
print(hashes)
print(sig_mat)

for i in range(len(sig_mat[0])):
  for j in range(len(sig_mat[0])):
    if i != j:
      print(f"{i}, {j} = {compare_signatures(sig_mat[:, i], sig_mat[:, j])}")