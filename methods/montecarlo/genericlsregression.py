def genericLongstaffSchwartzRegression(simulationData, basisCoefficients):
    steps = simulationData.size()
    basisCoefficients.resize(steps - 1)
    for i in range(steps - 1, 0, -1):
        exerciseData = simulationData[i]
        N = exerciseData.front().value.size()
        temp=[]
        stats=[]
        for j in range(0, exerciseData.size()):
            if exerciseData[j].isValid:
                temp = exerciseData[j].values
                #copy(exerciseData[j].values.begin(), exerciseData.values.end(), temp.begin())
                temp[-1] = exerciseData[j].cumulationCashFlows - exerciseData[j].controlValue
                stats.append(temp)
        means = sum(stats)/len(stats)
        covariance = stats.covarience()
        C=[]
        target=[]
        for k in range(N):
            target[k] = covariance[k][N] + means[k] * means[N]
            for l in range(k):
                C[k][l] = C[l][k] = covariance[k][l] + means[k] * means[l]
        alphas = SVD(C).solveFor(target)
        basisCoefficients[i - 1].resize(N)
        basisCoefficients[i - 1] = alphas
        #copy(alphas.begin(), alphas.end(), basisCoefficients[i - 1].begin())
        for j in range(exerciseData.size()):
            if exerciseData[j].isValid:
                exerciseValue = exerciseData[j].ecerciseValue
                continuationValue = exerciseData[j].cumulationCashFlows
                estimateContinuationValue = inner_product(exerciseData[j].values.begin(), exerciseData[j].values.end(),
                                                      alphas.begin(), exerciseData[j].controlValue)
                value = exerciseValue if estimateContinuationValue<=exerciseValue else continuationValue
                simulationData[i-1][j].cumulatedCashFlows += value
    estimateData = simulationData[0]
    estimate = []
    for j in range(estimateData.size()):
        estimate.append(estimateData[j].cumulatedCashFlows)
    return sum(estimate)/len(estimate)
