# Factor I: Codebase

## One codebase tracked in revision control, many deploys

### Implementation in Python Boyce

This application follows the single codebase principle:

- **Single Repository**: All code is maintained in one Git repository
- **Multiple Deployments**: The same codebase can be deployed to:
  - Development environment
  - Staging environment  
  - Production environment

### Key Files

- `.git/` - Version control tracking
- `app.py` - Main application code
- `requirements.txt` - Dependencies

### Best Practices

1. Use Git for version control
2. Never have multiple codebases for one app
3. Deploy the same codebase to all environments
4. Use branches for feature development
5. Tag releases for deployment tracking

### Environment Variables Used

- `ENVIRONMENT` - Identifies which deployment (dev/staging/prod)
- `APP_VERSION` - Tracks the deployed version

### Verification

Check the current codebase status:
```bash
git status
git log --oneline -5
```