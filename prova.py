from model.LocalRepoModel import LocalRepoModel

local = LocalRepoModel()
local.RepoDataUpdate()
print(local.getRepoData().name)