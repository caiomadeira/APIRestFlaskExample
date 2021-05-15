from API.suport import convertTxtToJson

file = convertTxtToJson()


def callLane(lane=file['lane']):
    return lane


def callVersion(version=file['version']):
    return version


def callEnv(env=file['env']):
    return env
