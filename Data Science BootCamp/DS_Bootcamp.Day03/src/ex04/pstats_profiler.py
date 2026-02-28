import cProfile
import pstats
import subprocess

profiler = cProfile.Profile()
profiler.enable()
subprocess.run(["python3", "financial_enhanced.py", "MSFT", "Total Revenue"])

profiler.disable()


stats = pstats.Stats(profiler)

stats.sort_stats("tottime")

stats.print_stats(5)
