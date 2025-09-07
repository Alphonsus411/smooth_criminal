import * as assert from 'assert';
import * as vscode from 'vscode';

describe('Extension Tests', () => {
    it('comando registrado', async () => {
        const commands = await vscode.commands.getCommands(true);
        assert.ok(commands.includes('smooth-criminal.analyze'));
    });
});
