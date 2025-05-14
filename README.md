# teamsbot
salple

# Connect bot to Azure
✅ Steps to allow sideloading (custom app installation) only for yourself in Microsoft Teams Admin Center
## 1. Go to Microsoft Teams Admin Center
https://admin.teams.microsoft.com

## 2. Check organization-wide settings for custom app uploads
  Navigate to:
  `Teams apps → Manage apps`
  
  In the top right corner, select Org-wide app settings.
  
  Make sure:
  
  Allow users to upload custom apps = On
  
  You can keep Allow interaction with custom apps only in certain policies = Off.

## 3. Create or edit a personal App Setup Policy
  Go to:
  `Teams apps → Setup policies`
  
  Create a new policy (e.g. Custom Policy - Personal Bot Testing) or edit an existing one.
  
  In this policy:
  
  Allow users to upload custom apps = On
  
  You can leave the Installed apps section empty (no apps added).
  
  Save the policy.

## 4. Assign the policy only to yourself
  Go to:
  `Users → Find your user account`
  
  In the Policies section, assign:
  
  App setup policy → Custom Policy - Personal Bot Testing
