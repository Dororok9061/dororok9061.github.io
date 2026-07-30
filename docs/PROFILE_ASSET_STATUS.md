# Profile Asset Status

Status: `BLOCKED`

The formal profile photograph is stored in a protected OneDrive location. The
source was not opened, copied, modified, or uploaded during this work.

The public GitHub avatar was inspected as an alternative and rejected because
it is an illustrated character, not the supplied formal portrait. No generated
or substituted face was used.

The site currently uses a non-biometric `HR` monogram. This preserves truthful
identity without exposing the wrong person or altering facial features.

## Required input to unblock

Provide a user-approved copy outside OneDrive in a workspace path. The
processing step will:

1. preserve the original
2. strip EXIF/XMP and embedded thumbnails
3. create an 800×800 square crop
4. create a portrait crop at approximately 900×1100 or the original ratio
5. export WebP quality about 85 with PNG/JPEG fallbacks
6. verify that no facial, skin, eye, clothing, or background generation occurred

