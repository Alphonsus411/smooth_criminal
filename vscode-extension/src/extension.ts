import * as vscode from 'vscode';
import * as cp from 'child_process';

export function activate(context: vscode.ExtensionContext) {
    const disposable = vscode.commands.registerCommand('smooth-criminal.analyze', async () => {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            vscode.window.showInformationMessage('No hay un editor activo.');
            return;
        }

        const code = editor.document.getText();
        const script = `
import ast, sys
from smooth_criminal.analizer import ASTAnalyzer
code = sys.stdin.read()
tree = ast.parse(code)
a = ASTAnalyzer()
a.visit(tree)
for f in a.findings:
    print(f)
`;

        try {
            const result = await runPython(script, code);
            if (result.trim().length === 0) {
                vscode.window.showInformationMessage('Sin sugerencias.');
            } else {
                result.split('\n').forEach(line => {
                    vscode.window.showInformationMessage(`@smooth ${line} @jam`);
                });
            }
        } catch (err: any) {
            vscode.window.showErrorMessage(`Error al analizar: ${err.message}`);
        }
    });

    context.subscriptions.push(disposable);
}

async function runPython(script: string, code: string): Promise<string> {
    return new Promise((resolve, reject) => {
        const proc = cp.spawn('python', ['-c', script]);
        let out = '';
        let err = '';
        proc.stdout.on('data', d => out += d.toString());
        proc.stderr.on('data', d => err += d.toString());
        proc.on('error', reject);
        proc.on('close', code => {
            if (code === 0) {
                resolve(out);
            } else {
                reject(new Error(err));
            }
        });
        proc.stdin.write(code);
        proc.stdin.end();
    });
}

export function deactivate() {}
