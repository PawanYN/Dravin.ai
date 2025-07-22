##### Sensitive Files Accidentally Committed



* Issue: Committed .env file and OpenAI API key.
* Effect: GitHub blocked the push due to secret scanning.
* Solution: Removed sensitive files from history using git rm --cached, and added .env to .gitignore.



##### .gitignore Not Working Properly



* Issue: venv/ folder was still being tracked.
* Real Cause: Hidden or malformed characters in .gitignore (from shell GUI or copy-paste).
* Solution: Manually rewrote venv/ line and verified it with git check-ignore -v.



##### Multiple .gitignore Files Created Confusion



* Issue: Conflicting or missing ignore rules due to .gitignore files in subfolders.
* Solution: Tracked all .gitignore files using:

  find . -name ".gitignore"

  find . -name ".gitignore" -exec grep -H . {} \\;

  find . -type f | git check-ignore -v --stdin



##### Branch \& Remote Mismatch



* Issue: Local branch was master, but remote expected main.
* Solution: Renamed local branch and set upstream remote using:



  git branch -M main

  git remote add origin <url>

  git push --set-upstream origin main

 

##### Deleted Entire Git History to Remove Sensitive Data



* Reason: API key was present in earlier commits.
* Solution: Deleted .git/ folder using **rm -rf .git**, then reinitialized the repo and recommitted clean files.
