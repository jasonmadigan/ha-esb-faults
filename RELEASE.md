# Release Process

Sample release process, in this example we're releasing `1.0.4`.

1. **Versioning**
   ```bash
   sed -i '' 's/"version": "[^"]*"/"version": "1.0.4"/' custom_components/esb_faults/manifest.json
   sed -i '' 's/"hacs": "[^"]*"/"hacs": "1.0.4"/' hacs.json
   ```

2. **Tag**
   ```bash
   git tag 1.0.4
   git push origin 1.0.4
   ```

3. **Create GitHub Release**
   - Go to https://github.com/jasonmadigan/ha-esb-faults/releases
   - Click "Create a new release"
   - Select the tag created above
   - Add release notes
   - Publish release