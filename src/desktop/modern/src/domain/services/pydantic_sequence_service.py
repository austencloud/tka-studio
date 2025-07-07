"""
Pydantic-based Sequence Service

This service demonstrates how to integrate the new Pydantic domain models
with the existing TKA service architecture while maintaining:

1. Clean Architecture principles
2. Immutability contracts
3. camelCase JSON serialization
4. Type safety and validation
5. Backward compatibility during migration

Key Features:
- Uses new Pydantic models internally
- Provides camelCase JSON API
- Maintains immutability (all operations return new objects)
- Full type safety with Pydantic validation
- Compatible with existing service interfaces
"""

from typing import List, Optional, Dict, Any
import json
from datetime import datetime

from ..models.pydantic_models import (
    MotionData,
    BeatData,
    SequenceData,
    create_default_motion_data,
    create_default_beat_data,
    create_default_sequence_data,
)


class PydanticSequenceService:
    """
    Sequence management service using Pydantic models.
    
    This service provides:
    - CRUD operations for sequences
    - Immutable operations (all methods return new objects)
    - camelCase JSON serialization
    - Type-safe validation
    - Clean error handling
    """
    
    def __init__(self):
        """Initialize the sequence service."""
        self._sequences: Dict[str, SequenceData] = {}
    
    # Sequence CRUD Operations
    
    def create_sequence(
        self, 
        name: str, 
        length: int = 8,
        difficulty: Optional[str] = None
    ) -> SequenceData:
        """
        Create a new sequence with default beats.
        
        Args:
            name: Sequence name
            length: Number of beats (default: 8)
            difficulty: Optional difficulty level
            
        Returns:
            New SequenceData object
            
        Raises:
            ValueError: If name is empty or length is invalid
        """
        if not name.strip():
            raise ValueError("Sequence name cannot be empty")
        
        if length < 1:
            raise ValueError("Sequence length must be at least 1")
        
        sequence = create_default_sequence_data(name, length)
        if difficulty:
            sequence = sequence.model_copy(update={'difficulty': difficulty})
        
        # Add timestamp
        now = datetime.now().isoformat()
        sequence = sequence.model_copy(update={
            'created_at': now,
            'updated_at': now
        })
        
        self._sequences[name] = sequence
        return sequence
    
    def get_sequence(self, name: str) -> Optional[SequenceData]:
        """
        Retrieve a sequence by name.
        
        Args:
            name: Sequence name
            
        Returns:
            SequenceData if found, None otherwise
        """
        return self._sequences.get(name)
    
    def list_sequences(self) -> List[SequenceData]:
        """
        List all sequences.
        
        Returns:
            List of all SequenceData objects
        """
        return list(self._sequences.values())
    
    def update_sequence(self, name: str, **updates) -> Optional[SequenceData]:
        """
        Update a sequence with new properties.
        
        Args:
            name: Sequence name
            **updates: Properties to update
            
        Returns:
            Updated SequenceData if found, None otherwise
        """
        sequence = self._sequences.get(name)
        if not sequence:
            return None
        
        # Add updated timestamp
        updates['updated_at'] = datetime.now().isoformat()
        
        updated_sequence = sequence.model_copy(update=updates)
        self._sequences[name] = updated_sequence
        return updated_sequence
    
    def delete_sequence(self, name: str) -> bool:
        """
        Delete a sequence.
        
        Args:
            name: Sequence name
            
        Returns:
            True if deleted, False if not found
        """
        if name in self._sequences:
            del self._sequences[name]
            return True
        return False
    
    # Beat Operations
    
    def add_beat(
        self, 
        sequence_name: str, 
        beat: BeatData,
        position: Optional[int] = None
    ) -> Optional[SequenceData]:
        """
        Add a beat to a sequence.
        
        Args:
            sequence_name: Target sequence name
            beat: BeatData to add
            position: Insert position (None = append)
            
        Returns:
            Updated SequenceData if successful, None if sequence not found
        """
        sequence = self._sequences.get(sequence_name)
        if not sequence:
            return None
        
        beats = sequence.beats.copy()
        
        if position is None:
            beats.append(beat)
        else:
            beats.insert(position, beat)
        
        updated_sequence = sequence.model_copy(update={
            'beats': beats,
            'updated_at': datetime.now().isoformat()
        })
        
        self._sequences[sequence_name] = updated_sequence
        return updated_sequence
    
    def update_beat(
        self, 
        sequence_name: str, 
        beat_index: int, 
        beat: BeatData
    ) -> Optional[SequenceData]:
        """
        Update a beat in a sequence.
        
        Args:
            sequence_name: Target sequence name
            beat_index: Index of beat to update
            beat: New BeatData
            
        Returns:
            Updated SequenceData if successful, None if sequence/beat not found
        """
        sequence = self._sequences.get(sequence_name)
        if not sequence or beat_index >= len(sequence.beats):
            return None
        
        beats = sequence.beats.copy()
        beats[beat_index] = beat
        
        updated_sequence = sequence.model_copy(update={
            'beats': beats,
            'updated_at': datetime.now().isoformat()
        })
        
        self._sequences[sequence_name] = updated_sequence
        return updated_sequence
    
    def remove_beat(
        self, 
        sequence_name: str, 
        beat_index: int
    ) -> Optional[SequenceData]:
        """
        Remove a beat from a sequence.
        
        Args:
            sequence_name: Target sequence name
            beat_index: Index of beat to remove
            
        Returns:
            Updated SequenceData if successful, None if sequence/beat not found
        """
        sequence = self._sequences.get(sequence_name)
        if not sequence or beat_index >= len(sequence.beats):
            return None
        
        beats = sequence.beats.copy()
        beats.pop(beat_index)
        
        updated_sequence = sequence.model_copy(update={
            'beats': beats,
            'updated_at': datetime.now().isoformat()
        })
        
        self._sequences[sequence_name] = updated_sequence
        return updated_sequence
    
    # JSON Serialization (camelCase)
    
    def sequence_to_json(self, sequence: SequenceData) -> str:
        """
        Convert sequence to camelCase JSON.
        
        Args:
            sequence: SequenceData to serialize
            
        Returns:
            JSON string with camelCase properties
        """
        return sequence.model_dump_json(indent=2)
    
    def sequence_from_json(self, json_str: str) -> SequenceData:
        """
        Create sequence from camelCase JSON.
        
        Args:
            json_str: JSON string with camelCase properties
            
        Returns:
            SequenceData object
            
        Raises:
            ValueError: If JSON is invalid or doesn't match schema
        """
        data = json.loads(json_str)
        return SequenceData(**data)
    
    def export_sequence(self, sequence_name: str) -> Optional[str]:
        """
        Export sequence as camelCase JSON.
        
        Args:
            sequence_name: Name of sequence to export
            
        Returns:
            JSON string if sequence found, None otherwise
        """
        sequence = self._sequences.get(sequence_name)
        if not sequence:
            return None
        
        return self.sequence_to_json(sequence)
    
    def import_sequence(self, json_str: str) -> SequenceData:
        """
        Import sequence from camelCase JSON.
        
        Args:
            json_str: JSON string with camelCase properties
            
        Returns:
            Imported SequenceData object
            
        Raises:
            ValueError: If JSON is invalid or doesn't match schema
        """
        sequence = self.sequence_from_json(json_str)
        self._sequences[sequence.name] = sequence
        return sequence
    
    # Utility Methods
    
    def create_sample_sequence(self, name: str = "Sample Sequence") -> SequenceData:
        """
        Create a sample sequence with some beats for testing.
        
        Args:
            name: Sequence name
            
        Returns:
            SequenceData with sample beats
        """
        sequence = self.create_sequence(name, length=4)
        
        # Add some sample beats
        for i in range(4):
            blue_motion = create_default_motion_data(
                motion_type='pro' if i % 2 == 0 else 'anti',
                start_loc='n' if i < 2 else 's',
                end_loc='e' if i % 2 == 0 else 'w'
            )
            
            red_motion = create_default_motion_data(
                motion_type='anti' if i % 2 == 0 else 'pro',
                start_loc='s' if i < 2 else 'n',
                end_loc='w' if i % 2 == 0 else 'e'
            )
            
            beat = create_default_beat_data(
                beat_number=i + 1,
                letter=chr(ord('A') + i),
                blue_motion=blue_motion,
                red_motion=red_motion
            )
            
            sequence = self.add_beat(name, beat)
        
        return sequence
    
    def get_sequence_stats(self, sequence_name: str) -> Optional[Dict[str, Any]]:
        """
        Get statistics about a sequence.
        
        Args:
            sequence_name: Name of sequence
            
        Returns:
            Dictionary with sequence statistics, None if not found
        """
        sequence = self._sequences.get(sequence_name)
        if not sequence:
            return None
        
        motion_types = []
        for beat in sequence.beats:
            motion_types.extend([
                beat.blue_motion.motion_type,
                beat.red_motion.motion_type
            ])
        
        return {
            'name': sequence.name,
            'beatCount': len(sequence.beats),
            'totalMotions': len(motion_types),
            'motionTypeDistribution': {
                motion_type: motion_types.count(motion_type)
                for motion_type in set(motion_types)
            },
            'createdAt': sequence.created_at,
            'updatedAt': sequence.updated_at,
            'difficulty': sequence.difficulty,
            'tags': sequence.tags
        }
