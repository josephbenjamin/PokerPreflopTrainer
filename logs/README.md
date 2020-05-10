This otherwise empty directory is present to ensure that the program can create a default log file here, without including the creator's own logs in any commits.

If writer.csv(path_to_log) should in fact be able to also create a directory, this would not be needed. However, in my testing, the log file was not created unless the logs folder was present.
