import os
import datetime
import yaml

class ProgressiveSummarizer:
    def __init__(self, memory_dir=".claude-memory"):
        self.memory_dir = memory_dir
        self.summaries_dir = os.path.join(memory_dir, "summaries")
        
    def create_session_summary(self, session_id, changes, decisions):
        """Create a summary of a coding session"""
        summary = {
            'session_id': session_id,
            'timestamp': datetime.datetime.now().isoformat(),
            'changes': changes,
            'decisions': decisions,
            'files_modified': list(set([c['file'] for c in changes]))
        }
        
        filename = f"session-{session_id}.yaml"
        filepath = os.path.join(self.summaries_dir, filename)
        
        with open(filepath, 'w') as f:
            yaml.dump(summary, f)
        
        return summary
