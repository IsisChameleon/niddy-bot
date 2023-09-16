Lots of problem getting this to work

pay attention to settings.json



    "python.defaultInterpreterPath": "/workspaces/niddy-bot/.venv/bin/python",
    "python.terminal.activateEnvInCurrentTerminal": true,
    "python.analysis.extraPaths": [
        "./src/modules"
    ],
    "python.envFile": "${workspaceFolder}/src/tests/.env",

    "python.testing.unittestEnabled": true,
    "python.testing.pytestEnabled": false,
    // "python.testing.unittestArgs": [
    //     "-v",
    //     "-s",
    //     "./src/tests",
    //     "-p",
    //     "test_*.py"
    // ],
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "/workspaces/niddy-bot/src/tests",
        "-p",
        "test_*.py"
    ]


Pay attention to env variables

(niddy-bot-py3.11) vscode ➜ /workspaces/niddy-bot (main) $ export PYTHONPATH=$PYTHONPATH:/workspaces/niddy-bot/src
(niddy-bot-py3.11) vscode ➜ /workspaces/niddy-bot (main) $ export PYTHONPATH=$PYTHONPATH:/workspaces/niddy-bot/src/tests