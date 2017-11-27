This is a short overview of the most important Git commands.

## Clone

To grab a complete copy of the github repository, use git clone like this:

```
git clone https://github.com/joelsonderegger/twitterbitcoin.git
```

Use this once at the beginning to get all the project's code.

Use this command at the location (in your terminal) where you want to have the project folder.


## Fetch

Use git fetch to retrieve new work done by other people. Fetching from a repository grabs all the new remote-tracking branches and tags without merging those changes into your own branches.

```
git fetch remotename
# Fetches updates made to a remote repository
```

Example:
```
git fetch origin
```

## Merge

Merging combines your local changes with changes made by others.

Typically, you'd merge a remote-tracking branch (i.e., a branch fetched from the remote repository) with your local branch:

```
git merge remotename/branchname
# Merges updates made online with your local work
```

Example:
```
git merge origin/master
```

## Pull
git pull is a convenient shortcut for completing both git fetch and git mergein the same command:

```
git pull remotename branchname
# Grabs online updates and merges them with your local work
```

Example:
```
git pull origin master
```

## Push
Use git push to push commits made on your local branch to a remote repository.

The git push command takes two arguments:

- A remote name, for example, origin
- A branch name, for example, master

```
git push  <REMOTENAME> <BRANCHNAME>
```

Example:
```
git push origin master
```

Remember that you have to first commit changes before being able to push them.

## CD

To use all the above mentioned functions you need to make sure, that you are in the right directionary. CD stands for change direction. Make sure that you are in the right folder.

Example for going forward:
```
cd desktop
```
Example for going backward:
```
cd ..
```
