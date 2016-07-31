def msd(A, B):
	n = len(A)
	m = len(B)
	f = [[0] * (m + 1) for i in range(0, n + 1)]
	for i in range(0, n + 1):
		for j in range(0, m + 1):
			if i == 0 and j == 0:
				f[i][j] = 0
			else:
				f[i][j] = n
			
			if i - 1 >= 0:
				f[i][j] = min(f[i][j], f[i - 1][j] + 1)
			
			if j - 1 >= 0:
				f[i][j] = min(f[i][j], f[i][j - 1] + 1)
			
			if i - 1 >= 0 and j - 1 >= 0:
				if A[i - 1] == B[j - 1]:
					f[i][j] = min(f[i][j], f[i - 1][j - 1])
				else:
					f[i][j] = min(f[i][j], f[i - 1][j - 1] + 1)
	return float(f[n][m]) / n
