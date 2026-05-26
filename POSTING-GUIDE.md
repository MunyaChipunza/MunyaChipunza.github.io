# Posting A New Reflection

Use the files in `G:\My Drive\100. Zee\Munyachipunza.com`.

1. Open `PASTE NEW POST IN HERE.txt`.
2. Replace the template with your post.
3. Keep the first line as `TITLE: Your title`.
4. Optional: set `TAG: Faith`, `TAG: Healing`, etc.
5. Leave a blank line between paragraphs.
6. Save the file.
7. Double-click `DOUBLE CLICK TO ACTIVATE NEW POST.bat`.

The script will use the clean publishing repo at `C:\Users\Dell\Projects\munya-publish`, generate the site, push it to GitHub Pages, wait for deployment, trigger the subscriber email, mirror the files back to Google Drive, then reset `PASTE NEW POST IN HERE.txt` for the next post.

## Optional Audio For Posts

If you want the site to generate a listenable MP3 for each new post:

1. Double-click `SET UP ELEVENLABS AUDIO.bat` once.
2. Paste your ElevenLabs API key.
3. Pick your cloned voice from the list and paste its `voice_id`.

After that, the normal `DOUBLE CLICK TO ACTIVATE NEW POST.bat` publisher will generate audio for new posts automatically.

To add audio to older posts, double-click `GENERATE AUDIO FOR POSTS.bat`. This uses ElevenLabs credits for every post that does not already have an MP3.
