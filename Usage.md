Usage:
1. Start an application in Eclipse/AndroidStudio
2. Switch to DDMS page
3. Click “Start Method Profiling”
4. *** Perform any operation you want on your phone ***
5. Click “Stop Method Profiling”
6. Save the traceview file to input.trace
7. Goto the directory of that file
8. python parse.py input.trace
9. perl FlameGraph-master/flamegraph result.txt > output.svg
