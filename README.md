# Pack Ventures Exercise
## How to run the code
1. Create your own virtual environment:
   ```bash
   python -m venv venv
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
3. Run the project:
   ```bash
   python main.py

## My approach to this problem:
My initial idea was to simply pass each company name to Gemini and ask for the founders. I realized that wouldn’t be reliable because AI models may be outdated and won’t necessarily reflect what’s written on the company’s own website. So I adjusted the approach: I first extract text directly from the company’s site—specifically the “About,” “Team,” and “Founders” pages (for example, /about, /team, and /founders). I chose these sections after checking where founder information usually appears. By feeding only this on-site text to the AI, the results stay grounded in what the company publicly states and more accurately identify the founders.

## Future Improvements:
- Although not listed in companies.txt, some companies may put founder info on pages other than “About,” “Team,” and “Founders.” I need to make sure the tool can find founder information even when it’s on unexpected pages.
- For example, on https://www.casium.com/ the founder information is inside a YouTube video. In the future, I want to make sure information in any format (video, images, etc.) can be read by the AI to identify the founders.
- Add a frontend to the code. Right now everything prints in the terminal, so it would be nice to have a simple website where you can type a company name and get the founders.
- Train my own model. Relying on Gemini is great, but for deployment it would be better to have a model tailored to this specific job (or fine-tuned for it).
   

